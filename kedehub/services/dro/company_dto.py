from typing import Optional
from pydantic import BaseModel
from kedehub.services.dro.project_dto import Project


class Company(BaseModel):

    company_name: str

    class Config:
        from_attributes = True