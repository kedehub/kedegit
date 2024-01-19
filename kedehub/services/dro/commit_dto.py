from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Json

from kedehub.utility.time_utility import _time_offset_to_local_time


class Commit(BaseModel):

    hexsha : str
    author_name : str
    added_lines : int
    added_chars : int
    deleted_lines : int
    deleted_chars : int
    lang_count: Dict
    commit_time : datetime
    commit_time_utc_offset : int
    parent_ids : Any = None
    repository_id : int

    def commit_time_tz(self):
        return _time_offset_to_local_time(self.commit_time, self.commit_time_utc_offset)

    class Config:
        from_attributes = True