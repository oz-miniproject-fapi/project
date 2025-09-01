# app/schemas/diary.py
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class DiaryCreate(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(...)
    tags: Optional[List[str]] = Field(default=[])
    emotion_keywords: Optional[List[str]] = Field(default=[])

class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = Field(None)
    tags: Optional[List[str]] = None
    emotion_keywords: Optional[List[str]] = None

class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str] = []
    emotion_keywords: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
