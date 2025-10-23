from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TopElementInfo(BaseModel):
    id: int
    points: int


class ChipPlay(BaseModel):
    chip_name: str
    num_played: int


class Overrides(BaseModel):
    rules: Dict[str, Any] = Field(default_factory=dict)
    scoring: Dict[str, Any] = Field(default_factory=dict)
    element_types: List[Any] = Field(default_factory=list)
    pick_multiplier: Optional[float] = None


class Event(BaseModel):
    id: int
    name: str
    deadline_time: datetime
    release_time: Optional[datetime]
    average_entry_score: int
    finished: bool
    data_checked: bool
    highest_scoring_entry: Optional[int]
    deadline_time_epoch: int
    deadline_time_game_offset: int
    highest_score: Optional[int]
    is_previous: bool
    is_current: bool
    is_next: bool
    cup_leagues_created: bool
    h2h_ko_matches_created: bool
    can_enter: bool
    can_manage: bool
    released: bool
    ranked_count: int
    overrides: Overrides
    chip_plays: List[ChipPlay]
    most_selected: Optional[int]
    most_transferred_in: Optional[int]
    top_element: Optional[int]
    top_element_info: Optional[TopElementInfo]
    transfers_made: Optional[int]
    most_captained: Optional[int]
    most_vice_captained: Optional[int]
    ingestion_time: Optional[datetime] = None
