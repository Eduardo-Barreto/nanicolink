from typing import Optional
from pydantic import BaseModel


class RequestLink(BaseModel):
    long_url: str
    keyword: Optional[str] = ''
    tags: Optional[list] = []
    destroy_clicks: Optional[int] = 0
    destroy_time: Optional[float] = 0


class Keyword(BaseModel):
    keyword: str


class ResponseLink(BaseModel):
    long_url: str
    keyword: str
    clicks: int
    destroy_clicks: int
    tags: list
    date_created: float
    destroy_time: float
