from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EventChannelModel(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

    @field_validator("title")
    def is_alphanumeric_title(cls, v):
        if not v.isalnum():
            raise ValueError("title must contain only alphanumeric characters")
        return v

    @field_validator("id")
    def is_alphanumeric_name(cls, v):
        if not v.isalnum():
            raise ValueError("id must contain only alphanumeric characters")
        return v

    @field_validator("description")
    def is_alphanumeric_description(cls, v):
        if v is not None and not v.isalnum():
            raise ValueError("description must contain only alphanumeric characters")
        return v

    def get_channel_id(self) -> str:
        return self.ti
