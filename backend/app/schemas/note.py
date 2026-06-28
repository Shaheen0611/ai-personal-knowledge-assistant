import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class NoteCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255, 
    )

    content: str = Field(
        min_length=1,
    )

class NoteUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    content: str | None = Field(
        default=None,
        min_length=1
    )

class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime