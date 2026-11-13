from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass


@dataclass
class Media:
    id: str
    name: str
    category: str
    country: str
    date: int = Field(ge=1895, le=2026)
    time: int = Field(gt=0)

    @field_validator("id", "name", "category", "country")
    @classmethod
    def validate(cls, item: str) -> str:
        if not item.strip():
            raise ValueError
        return item
