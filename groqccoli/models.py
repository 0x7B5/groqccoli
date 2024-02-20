import pydantic
from typing import Optional


class Stats(pydantic.BaseModel):
    time_generated: float
    tokens_generated: int
    time_processed: float
    tokens_processed: int


class Chat(pydantic.BaseModel):
    content: str
    request_id: Optional[str]
    stats: Stats
