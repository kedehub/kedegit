from pydantic import BaseModel
from typing import Optional

class MatchingBlacklist(BaseModel):
    excluded: Optional[str] = None

    class Config:
        from_attributes = True