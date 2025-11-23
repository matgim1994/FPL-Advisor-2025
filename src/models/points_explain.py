from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PointsExplain(BaseModel):
    id: int
    fixture: int
    identifier: str
    points: int
    value: int
    points_modification: int
    data_hash: Optional[str] = None
    ingestion_time: Optional[datetime] = None
