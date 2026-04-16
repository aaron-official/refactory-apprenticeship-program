"""
Pydantic Schemas
----------------
Defines data models for request validation and response serialization.
"""
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    done: bool = False

class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        from_attributes = True