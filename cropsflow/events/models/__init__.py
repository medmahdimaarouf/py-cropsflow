from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EventChannelModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

    @field_validator("name")
    def is_alphanumeric_name(cls, v: str):
        if v is not None and not v.replace(' ', '').strip().isalnum():
            raise ValueError("name must contain only alphanumeric characters")
        return v

    def get_channel_id(self) -> str:
        return self.name.strip().replace(' ', '-').lower()


class EventChannelEventModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

    @field_validator("name")
    def is_alphanumeric_title(cls, v: str):
        if v is not None and not v.replace(' ', '').strip().isalnum():
            raise ValueError("title must contain only alphanumeric characters")
        return v

    def get_id(self) -> str:
        return self.name.strip().replace(' ', '-').lower()
