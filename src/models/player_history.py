from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PlayerHistory(BaseModel):
    element: int
    fixture: int
    opponent_team: int
    total_points: int
    was_home: bool
    kickoff_time: datetime
    team_h_score: int
    team_a_score: int
    round: int
    modified: bool
    minutes: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int
    bps: int
    influence: float
    creativity: float
    threat: float
    ict_index: float
    clearances_blocks_interceptions: int
    recoveries: int
    tackles: int
    defensive_contribution: int
    starts: int
    expected_goals: float
    expected_assists: float
    expected_goal_involvements: float
    expected_goals_conceded: float
    value: int
    transfers_balance: int
    selected: int
    transfers_in: int
    transfers_out: int
    ingestion_time: Optional[datetime] = None
