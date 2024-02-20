import pydantic


class Stats(pydantic.BaseModel):
    time_generated: float
    tokens_generated: int
    time_processed: float
    tokens_processed: int


class Chat(pydantic.BaseModel):
    content: str
    request_id: str
    stats: Stats
