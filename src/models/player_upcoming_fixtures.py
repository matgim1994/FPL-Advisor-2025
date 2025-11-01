from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PlayerFixtures(BaseModel):
    id: int
    code: int
    team_h: int
    team_h_score: Optional[int]
    team_a: int
    team_a_score: Optional[int]
    event: int
    finished: bool
    minutes: int
    provisional_start_time: bool
    kickoff_time: datetime
    event_name: str
    is_home: bool
    difficulty: int
    ingestion_time: Optional[datetime] = None
