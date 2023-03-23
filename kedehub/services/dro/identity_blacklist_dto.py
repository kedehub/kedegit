from pydantic import BaseModel
from typing import Optional

class MatchingBlacklist(BaseModel):
    excluded: Optional[str] = None

    class Config:
        orm_mode = True