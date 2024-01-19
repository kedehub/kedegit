from asyncio import get_event_loop
from typing import IO, TYPE_CHECKING, Awaitable, List
from kedehub.services.dro.project_dto import Project
from kedehub.services.dro.project_repository_dto import ProjectRepository
from kedehub_client import server_config

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient


class _ProjectApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_list_all_project_names(self, company: str) -> Awaitable[List[str]]:
        url = '/companies/' + company + "/projects"
        return self.api_client.request(type_= List[str], method="GET", url= url)

    def _build_for_add_new_project_repository(self, project_repository, company: str):
        url = '/companies/' + company +'/projects/'+ project_repository.project_name +'/repos/'+str(project_repository.repository_id)
        return self.api_client.request(type_= ProjectRepository, method="POST", url=url)

    def _build_for_save_project_if_not_exists(self, project, company: str):
        url = '/companies/' + company + '/projects'
        return self.api_client.request(type_= Project, method="POST", url=url, content =project.model_dump_json())



class AsyncProjectApi(_ProjectApi):
    pass

class SyncProjectApi(_ProjectApi):
    def load_all_project_names(self) -> List[str]:
        coroutine = self._build_for_list_all_project_names(server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def add_new_project_repository(self, project_name,repository_id):
        project_repository = ProjectRepository(
            project_name=project_name,
            repository_id=repository_id)
        coroutine = self._build_for_add_new_project_repository(project_repository, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def save_project_if_not_exists(self, project_name):
        company_name = server_config.get_company_name()
        project = Project(project_name = project_name,
                          company_name = server_config.get_company_name())
        coroutine = self._build_for_save_project_if_not_exists(project, company_name)
        return get_event_loop().run_until_complete(coroutine)