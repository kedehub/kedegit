from datetime import datetime
from typing import Optional, Any

from git import Repo
from pydantic import BaseModel

from kedehub.config import Configuration
from kedehub.utility.time_utility import _time_offset_to_local_time


class Repository(BaseModel):

    id : Optional[int] = None
    origin: str
    repository_path : Optional[str] = None
    configuration_file_path : Optional[str] = None
    head_commit_id : Optional[str] = None
    start_time : Optional[datetime] = None
    start_time_utc_offset : Optional[int] = None
    company_name : Optional[str] = None
    configuration : Optional[Any] = None
    git_repository : Optional[Any] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        # self._init_properties()

    def _init_properties(self):
        self.configuration = Configuration(self.configuration_file_path)
        self.git_repository = Repo(self.repository_path)

    def start_time_tz(self):
        if self.start_time:
            return _time_offset_to_local_time(self.start_time, self.start_time_utc_offset)
        else:
            return None

    class Config:
        from_attributes = True