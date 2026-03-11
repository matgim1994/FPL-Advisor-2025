import json
import pytest
import requests
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch, call

from src.models.team import Team
from src.models.event import Event


class TestComputeHash:
    """_compute_hash produces a deterministic SHA256 hex digest from selected fields."""

    def test_same_input_produces_same_hash(self, handler, sample_team_data):
        record = Team.model_validate(sample_team_data)
        hash_columns = ["id", "name", "points"]

        hash1 = handler._compute_hash(record, hash_columns)
        hash2 = handler._compute_hash(record, hash_columns)

        assert hash1 == hash2

    def test_different_value_produces_different_hash(self, handler, sample_team_data):
        record_a = Team.model_validate(sample_team_data)
        record_b = Team.model_validate({**sample_team_data, "points": 999})
        hash_columns = ["id", "name", "points"]

        assert handler._compute_hash(record_a, hash_columns) != handler._compute_hash(record_b, hash_columns)

    def test_excluded_column_does_not_affect_hash(self, handler, sample_team_data):
        """ingestion_time is always excluded from hashing — two records with different
        ingestion times but identical data should produce the same hash."""
        hash_columns = ["id", "name", "points"]

        record_a = Team.model_validate(sample_team_data)
        record_a.ingestion_time = datetime(2024, 1, 1, tzinfo=timezone.utc)

        record_b = Team.model_validate(sample_team_data)
        record_b.ingestion_time = datetime(2025, 6, 1, tzinfo=timezone.utc)

        assert handler._compute_hash(record_a, hash_columns) == handler._compute_hash(record_b, hash_columns)

    def test_returns_64_char_hex_string(self, handler, sample_team_data):
        record = Team.model_validate(sample_team_data)
        result = handler._compute_hash(record, ["id", "name"])

        assert isinstance(result, str)
        assert len(result) == 64


class TestSerializeArrays:
    """_serialize_arrays converts dict and list values to JSON strings in-place."""

    def test_dict_value_is_serialized(self, handler):
        record = {"stats": {"goals": 1}}
        handler._serialize_arrays(record)
        assert record["stats"] == json.dumps({"goals": 1})

    def test_list_value_is_serialized(self, handler):
        record = {"chip_plays": [{"chip_name": "bboost", "num_played": 10}]}
        handler._serialize_arrays(record)
        assert record["chip_plays"] == json.dumps([{"chip_name": "bboost", "num_played": 10}])

    def test_scalar_values_pass_through(self, handler):
        record = {"id": 1, "name": "Arsenal", "active": True}
        handler._serialize_arrays(record)
        assert record == {"id": 1, "name": "Arsenal", "active": True}

    def test_mixed_record(self, handler):
        record = {"id": 42, "metadata": {"key": "value"}, "tags": ["a", "b"]}
        handler._serialize_arrays(record)
        assert record["id"] == 42
        assert record["metadata"] == json.dumps({"key": "value"})
        assert record["tags"] == json.dumps(["a", "b"])


class TestApiCall:
    """_api_call wraps requests.get and returns parsed JSON."""

    def test_returns_parsed_json(self, handler):
        mock_response = MagicMock()
        mock_response.json.return_value = {"teams": [], "events": []}

        with patch("src.db_handlers.db_handler.requests.get", return_value=mock_response):
            result = handler._api_call("https://example.com/api")

        assert result == {"teams": [], "events": []}

    def test_re_raises_on_exception(self, handler):
        with patch("src.db_handlers.db_handler.requests.get", side_effect=ConnectionError("timeout")):
            with pytest.raises(ConnectionError, match="timeout"):
                handler._api_call("https://example.com/api")


class TestApiSession:
    """_api_session returns a requests.Session with the correct User-Agent header."""

    def test_returns_session(self, handler):
        session = handler._api_session()
        assert isinstance(session, requests.Session)

    def test_user_agent_header(self, handler):
        session = handler._api_session()
        assert session.headers["User-Agent"] == "FPL2025"


class TestGetPlayersIds:
    """_get_players_ids queries the DB and returns a flat list of player IDs."""

    def test_returns_list_of_ids(self, handler, mock_cursor):
        mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]

        result = handler._get_players_ids()

        assert result == [1, 2, 3]

    def test_logs_warning_when_below_threshold(self, handler, mock_cursor):
        # Return fewer than 746 players — a warning should be logged
        mock_cursor.fetchall.return_value = [(i,) for i in range(100)]

        with patch.object(handler._logger, "warning") as mock_warning:
            handler._get_players_ids()
            mock_warning.assert_called_once()

    def test_no_warning_when_above_threshold(self, handler, mock_cursor):
        mock_cursor.fetchall.return_value = [(i,) for i in range(800)]

        with patch.object(handler._logger, "warning") as mock_warning:
            handler._get_players_ids()
            mock_warning.assert_not_called()


class TestGetStartedEvents:
    """_get_started_events queries the DB and returns IDs of started/finished GWs."""

    def test_returns_list_of_gw_ids(self, handler, mock_cursor):
        mock_cursor.fetchall.return_value = [(1,), (2,), (5,)]

        result = handler._get_started_events()

        assert result == [1, 2, 5]

    def test_returns_empty_list_when_no_events_started(self, handler, mock_cursor):
        mock_cursor.fetchall.return_value = []

        result = handler._get_started_events()

        assert result == []


class TestUpsertRawData:
    """_upsert_raw_data builds and executes a PostgreSQL upsert statement."""

    def test_executemany_called_once(self, handler, mock_cursor, sample_team_data):
        records = [Team.model_validate(sample_team_data)]
        columns = list(Team.model_fields.keys())
        hash_columns = [c for c in columns if c != "ingestion_time"]
        ingestion_time = datetime.now(timezone.utc)

        handler._upsert_raw_data(
            schema="raw",
            table_name="teams",
            records=records,
            columns=columns,
            hash_columns=hash_columns,
            primary_keys=["id"],
            ingestion_time=ingestion_time,
        )

        mock_cursor.executemany.assert_called_once()

    def test_sql_contains_on_conflict(self, handler, mock_cursor, sample_team_data):
        records = [Team.model_validate(sample_team_data)]
        columns = list(Team.model_fields.keys())
        hash_columns = [c for c in columns if c != "ingestion_time"]
        ingestion_time = datetime.now(timezone.utc)

        handler._upsert_raw_data(
            schema="raw",
            table_name="teams",
            records=records,
            columns=columns,
            hash_columns=hash_columns,
            primary_keys=["id"],
            ingestion_time=ingestion_time,
        )

        sql = mock_cursor.executemany.call_args[0][0].lower()
        assert "on conflict" in sql
        assert "do update set" in sql
        assert "data_hash is distinct from" in sql

    def test_primary_key_not_in_set_clause(self, handler, mock_cursor, sample_team_data):
        records = [Team.model_validate(sample_team_data)]
        columns = list(Team.model_fields.keys())
        hash_columns = [c for c in columns if c != "ingestion_time"]
        ingestion_time = datetime.now(timezone.utc)

        handler._upsert_raw_data(
            schema="raw",
            table_name="teams",
            records=records,
            columns=columns,
            hash_columns=hash_columns,
            primary_keys=["id"],
            ingestion_time=ingestion_time,
        )

        sql = mock_cursor.executemany.call_args[0][0]
        # Extract the SET clause — everything after DO UPDATE SET
        set_clause = sql.split("do update set")[-1].split("where")[0].lower()
        # "id = excluded.id" should NOT be in the set clause
        assert "id = excluded.id" not in set_clause

    def test_record_data_hash_is_set(self, handler, mock_cursor, sample_team_data):
        record = Team.model_validate(sample_team_data)
        assert record.data_hash is None  # not set before calling upsert

        columns = list(Team.model_fields.keys())
        hash_columns = [c for c in columns if c != "ingestion_time"]
        ingestion_time = datetime.now(timezone.utc)

        handler._upsert_raw_data(
            schema="raw",
            table_name="teams",
            records=[record],
            columns=columns,
            hash_columns=hash_columns,
            primary_keys=["id"],
            ingestion_time=ingestion_time,
        )

        assert record.data_hash is not None


class TestUpdateEvents:
    """update_events fetches from API, validates with Pydantic, and calls upsert."""

    def test_calls_upsert_with_correct_table(self, handler, sample_event_data):
        api_response = {"events": [sample_event_data]}

        with patch.object(handler, "_api_call", return_value=api_response):
            with patch.object(handler, "_upsert_raw_data") as mock_upsert:
                handler.update_events()

        mock_upsert.assert_called_once()
        call_kwargs = mock_upsert.call_args.kwargs
        assert call_kwargs["schema"] == "raw"
        assert call_kwargs["table_name"] == "events"

    def test_re_raises_api_exception(self, handler):
        with patch.object(handler, "_api_call", side_effect=ConnectionError("API down")):
            with pytest.raises(ConnectionError, match="API down"):
                handler.update_events()

    def test_re_raises_on_invalid_api_data(self, handler):
        # Missing required fields in the event payload
        bad_response = {"events": [{"id": 1}]}  # far too few fields

        with patch.object(handler, "_api_call", return_value=bad_response):
            with pytest.raises(Exception):
                handler.update_events()
