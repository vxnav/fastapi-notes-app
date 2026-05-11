from pydantic import BaseModel, Field, AfterValidator
from enum import Enum
from datetime import datetime
from typing import Annotated

def check_string(value: str) -> str:
    if len(value.strip()) == 0:
        raise ValueError("Empty title or content")
    return value

class Note(BaseModel):
    # ... -> required field
    title: Annotated[str , AfterValidator(check_string)] = Field(..., min_length=1, max_length=100)
    content: Annotated[str, AfterValidator(check_string)] = Field(..., min_length=1, max_length=1000)

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