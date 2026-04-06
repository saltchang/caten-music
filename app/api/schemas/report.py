from datetime import datetime

from pydantic import BaseModel


class ReportCreateRequest(BaseModel):
    description: str
    song_sid: int


class ReportResponse(BaseModel):
    id: int
    description: str
    song_sid: int
    user_id: int
    reported_time: datetime
