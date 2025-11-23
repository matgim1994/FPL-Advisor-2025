from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StatEntry(BaseModel):
    value: int
    element: int


class Stat(BaseModel):
    identifier: str
    a: List[StatEntry]
    h: List[StatEntry]


class Fixture(BaseModel):
    code: int
    event: int
    finished: bool
    finished_provisional: bool
    id: int
    kickoff_time: datetime
    minutes: int
    provisional_start_time: bool
    started: bool
    team_a: int
    team_a_score: Optional[int]
    team_h: int
    team_h_score: Optional[int]
    stats: List[Stat]
    team_h_difficulty: int
    team_a_difficulty: int
    pulse_id: int
    data_hash: Optional[str] = None
    ingestion_time: Optional[datetime] = None
