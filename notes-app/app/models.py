from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class Note(BaseModel):
    # ... -> required field
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=1000)

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    createdAt: datetime
    updatedAt: datetime | None = None

class DeleteNote(BaseModel):
    message: str
    note: NoteResponse

class SortField(str, Enum):
    createdAt = "createdAt"
    updatedAt = "updatedAt"