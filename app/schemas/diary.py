from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# 일기 작성 요청용
class DiaryCreate(BaseModel):
    title: str
    content: str
    date: date

# 일기 수정 요청용 (PATCH)
class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    date: Optional[date] = None

# 일기 작성/조회 응답용
class DiaryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
