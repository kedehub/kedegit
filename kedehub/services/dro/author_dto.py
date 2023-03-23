
from typing import Optional, List

from pydantic import BaseModel, UUID4


class Author(BaseModel):
    canonical_name: str
    aliases: Optional[str] = None
    name : str
    email : str
    user_id : Optional[UUID4] = None

    class Config:
        orm_mode = True