from typing import Optional
from datetime import datetime

from pydantic.main import BaseModel


class Project(BaseModel):

    project_name : str
    start_date : Optional[datetime] = None
    company_name : str
    long_name : Optional[str] = None
    is_active : Optional[bool] = None
    is_private : Optional[bool] = None
    description : Optional[str] = None

    class Config:
        from_attributes = True