import uuid
from typing import Optional, List
from pydantic import UUID4, validator

from pydantic.main import BaseModel

from kedehub.services.dro.author_dto import Author


class User(BaseModel):

    id: Optional[UUID4] = None
    name : Optional[str] = None
    primary_email : Optional[str] = None
    is_active : Optional[bool] = True
    description: Optional[str] = None
    workplace: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    twitter: Optional[str] = None
    is_show_email: Optional[bool] = True
    identities: Optional[List[Author]] = list()

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()