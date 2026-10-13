from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class DocumentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filename: str = Field(max_length=50)
    storage_path: str = Field(max_length=200)
    content_type: str = Field(max_length=50)
    file_size: int = Field(ge=0)


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str = Field(max_length=50)
    storage_path: str = Field(max_length=200)
    content_type: str = Field(max_length=50)
    file_size: int = Field(ge=0)
    status: str = Field(max_length=50)
    error_message: str | None
    created_at: datetime
    updated_at: datetime
