from typing import Optional
from datetime import datetime

from pydantic.main import BaseModel


class Project(BaseModel):

    project_name : str
    start_date : Optional[datetime]
    company_name : str
    long_name : Optional[str]
    is_active : Optional[bool]
    is_private : Optional[bool]
    description : Optional[str]

    class Config:
        orm_mode = True