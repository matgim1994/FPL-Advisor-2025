import pytest
from pydantic import ValidationError

from src.models.team import Team
from src.models.event import Event
from src.models.fixture import Fixture
from src.models.player_history import PlayerHistory
from src.models.points_explain import PointsExplain


class TestTeamModel:

    def test_valid_data_validates(self, sample_team_data):
        team = Team.model_validate(sample_team_data)
        assert team.id == 1
        assert team.name == "Arsenal"
        assert team.short_name == "ARS"

    def test_optional_form_accepts_none(self, sample_team_data):
        sample_team_data["form"] = None
        team = Team.model_validate(sample_team_data)
        assert team.form is None

    def test_missing_required_field_raises(self, sample_team_data):
        del sample_team_data["name"]
        with pytest.raises(ValidationError):
            Team.model_validate(sample_team_data)


class TestEventModel:

    def test_valid_data_validates(self, sample_event_data):
        event = Event.model_validate(sample_event_data)
        assert event.id == 1
        assert event.name == "Gameweek 1"
        assert event.finished is True

    def test_optional_release_time_accepts_none(self, sample_event_data):
        sample_event_data["release_time"] = None
        event = Event.model_validate(sample_event_data)
        assert event.release_time is None

    def test_optional_top_element_info_accepts_none(self, sample_event_data):
        sample_event_data["top_element_info"] = None
        event = Event.model_validate(sample_event_data)
        assert event.top_element_info is None

    def test_chip_plays_parsed_as_list(self, sample_event_data):
        event = Event.model_validate(sample_event_data)
        assert isinstance(event.chip_plays, list)
        assert event.chip_plays[0].chip_name == "bboost"

    def test_missing_required_field_raises(self, sample_event_data):
        del sample_event_data["deadline_time"]
        with pytest.raises(ValidationError):
            Event.model_validate(sample_event_data)


class TestFixtureModel:

    def test_valid_data_validates(self, sample_fixture_data):
        fixture = Fixture.model_validate(sample_fixture_data)
        assert fixture.id == 1
        assert fixture.finished is True
        assert fixture.team_h == 1
        assert fixture.team_a == 2

    def test_optional_event_accepts_none(self, sample_fixture_data):
        sample_fixture_data["event"] = None
        fixture = Fixture.model_validate(sample_fixture_data)
        assert fixture.event is None

    def test_stats_parsed_as_list(self, sample_fixture_data):
        fixture = Fixture.model_validate(sample_fixture_data)
        assert isinstance(fixture.stats, list)
        assert fixture.stats[0].identifier == "goals_scored"

    def test_missing_required_field_raises(self, sample_fixture_data):
        del sample_fixture_data["team_h"]
        with pytest.raises(ValidationError):
            Fixture.model_validate(sample_fixture_data)


class TestPlayerHistoryModel:

    def test_valid_data_validates(self, sample_player_history_data):
        history = PlayerHistory.model_validate(sample_player_history_data)
        assert history.element == 350
        assert history.fixture == 1
        assert history.total_points == 12

    def test_optional_scores_accept_none(self, sample_player_history_data):
        sample_player_history_data["team_h_score"] = None
        sample_player_history_data["team_a_score"] = None
        history = PlayerHistory.model_validate(sample_player_history_data)
        assert history.team_h_score is None
        assert history.team_a_score is None

    def test_missing_required_field_raises(self, sample_player_history_data):
        del sample_player_history_data["element"]
        with pytest.raises(ValidationError):
            PlayerHistory.model_validate(sample_player_history_data)


class TestPointsExplainModel:

    def test_valid_data_validates(self, sample_points_explain_data):
        pe = PointsExplain.model_validate(sample_points_explain_data)
        assert pe.id == 350
        assert pe.fixture == 1
        assert pe.identifier == "goals_scored"
        assert pe.points == 4

    def test_missing_required_field_raises(self, sample_points_explain_data):
        del sample_points_explain_data["identifier"]
        with pytest.raises(ValidationError):
            PointsExplain.model_validate(sample_points_explain_data)
