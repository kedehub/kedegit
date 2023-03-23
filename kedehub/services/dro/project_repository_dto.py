from pydantic.main import BaseModel


class ProjectRepository(BaseModel):

    project_name : str
    repository_id: str