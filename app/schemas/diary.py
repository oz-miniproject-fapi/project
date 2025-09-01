from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class DiaryCreate(BaseModel):
    title: str
    content: str
    date: date

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    date: Optional[date] = None

class DiaryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
