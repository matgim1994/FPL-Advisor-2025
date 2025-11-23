from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Team(BaseModel):
    code: int
    draw: int
    form: Optional[str]
    id: int
    loss: int
    name: str
    played: int
    points: int
    position: int
    short_name: str
    strength: int
    team_division: Optional[str]
    unavailable: bool
    win: int
    strength_overall_home: int
    strength_overall_away: int
    strength_attack_home: int
    strength_attack_away: int
    strength_defence_home: int
    strength_defence_away: int
    pulse_id: int
    data_hash: Optional[str] = None
    ingestion_time: Optional[datetime] = None
