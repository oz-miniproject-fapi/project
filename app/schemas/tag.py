# app/schemas/tag.py
from pydantic import BaseModel

class TagCreate(BaseModel):
    name: str

class TagRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
