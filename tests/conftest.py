import pytest
from unittest.mock import MagicMock
from src.db_handlers.db_handler import DBHandler


@pytest.fixture
def mock_cursor():
    cursor = MagicMock()
    cursor.fetchall.return_value = []
    return cursor


@pytest.fixture
def mock_conn(mock_cursor):
    conn = MagicMock()
    # Make conn.cursor() work as a context manager: `with conn.cursor() as cur:`
    conn.cursor.return_value.__enter__.return_value = mock_cursor
    conn.cursor.return_value.__exit__.return_value = False
    return conn


@pytest.fixture
def handler(mock_conn):
    return DBHandler(pg_conn=mock_conn)


# --- Sample data fixtures ---
# These dicts mirror the raw FPL API response shape for each entity.

@pytest.fixture
def sample_team_data():
    return {
        "code": 3,
        "draw": 5,
        "form": None,
        "id": 1,
        "loss": 10,
        "name": "Arsenal",
        "played": 30,
        "points": 55,
        "position": 2,
        "short_name": "ARS",
        "strength": 4,
        "team_division": None,
        "unavailable": False,
        "win": 15,
        "strength_overall_home": 1270,
        "strength_overall_away": 1240,
        "strength_attack_home": 1280,
        "strength_attack_away": 1250,
        "strength_defence_home": 1260,
        "strength_defence_away": 1230,
        "pulse_id": 1,
    }


@pytest.fixture
def sample_event_data():
    return {
        "id": 1,
        "name": "Gameweek 1",
        "deadline_time": "2024-08-16T17:30:00Z",
        "release_time": None,
        "average_entry_score": 56,
        "finished": True,
        "data_checked": True,
        "highest_scoring_entry": 12345,
        "deadline_time_epoch": 1723826400,
        "deadline_time_game_offset": 0,
        "highest_score": 142,
        "is_previous": False,
        "is_current": False,
        "is_next": False,
        "cup_leagues_created": False,
        "h2h_ko_matches_created": False,
        "can_enter": False,
        "can_manage": False,
        "released": True,
        "ranked_count": 10000000,
        "overrides": {"rules": {}, "scoring": {}, "element_types": [], "pick_multiplier": None},
        "chip_plays": [{"chip_name": "bboost", "num_played": 500000}],
        "most_selected": 350,
        "most_transferred_in": 123,
        "top_element": 350,
        "top_element_info": {"id": 350, "points": 18},
        "transfers_made": 5000000,
        "most_captained": 350,
        "most_vice_captained": 123,
    }


@pytest.fixture
def sample_fixture_data():
    return {
        "code": 2412099,
        "event": 1,
        "finished": True,
        "finished_provisional": True,
        "id": 1,
        "kickoff_time": "2024-08-16T19:00:00Z",
        "minutes": 90,
        "provisional_start_time": False,
        "started": True,
        "team_a": 2,
        "team_a_score": 1,
        "team_h": 1,
        "team_h_score": 2,
        "stats": [
            {
                "identifier": "goals_scored",
                "a": [{"value": 1, "element": 100}],
                "h": [{"value": 2, "element": 200}],
            }
        ],
        "team_h_difficulty": 3,
        "team_a_difficulty": 4,
        "pulse_id": 99,
    }


@pytest.fixture
def sample_player_history_data():
    return {
        "element": 350,
        "fixture": 1,
        "opponent_team": 2,
        "total_points": 12,
        "was_home": True,
        "kickoff_time": "2024-08-16T19:00:00Z",
        "team_h_score": 2,
        "team_a_score": 1,
        "round": 1,
        "modified": False,
        "minutes": 90,
        "goals_scored": 1,
        "assists": 1,
        "clean_sheets": 0,
        "goals_conceded": 1,
        "own_goals": 0,
        "penalties_saved": 0,
        "penalties_missed": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "saves": 0,
        "bonus": 3,
        "bps": 42,
        "influence": 62.4,
        "creativity": 28.0,
        "threat": 55.0,
        "ict_index": 14.6,
        "clearances_blocks_interceptions": 0,
        "recoveries": 2,
        "tackles": 1,
        "defensive_contribution": 1,
        "starts": 1,
        "expected_goals": 0.45,
        "expected_assists": 0.31,
        "expected_goal_involvements": 0.76,
        "expected_goals_conceded": 0.55,
        "value": 85,
        "transfers_balance": 50000,
        "selected": 3000000,
        "transfers_in": 100000,
        "transfers_out": 50000,
    }


@pytest.fixture
def sample_points_explain_data():
    return {
        "id": 350,
        "fixture": 1,
        "identifier": "goals_scored",
        "points": 4,
        "value": 1,
        "points_modification": 0,
    }
