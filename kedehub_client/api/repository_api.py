from asyncio import get_event_loop
from typing import TYPE_CHECKING, List

from kedehub.services.dro.repository_dto import Repository
from kedehub_client import server_config
if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient

class _RepositoryApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_save_new_repository(self, repo, company):
        repo.company_name = company
        url = "/companies/"+company+"/repositories"
        return self.api_client.request(type_= Repository, method="POST", url=url,
                                       data =repo.json(exclude={'repository_path','configuration_file_path', 'configuration','git_repository'}))

    def _build_get_company_repositories(self, company):
        url = "/companies/"+company+"/repositories"
        return self.api_client.request(type_=List[Repository], method="GET", url=url)

    def _build_get_all_repositoriesy_for_project(self, company, project):
        url = "/companies/"+company+"/projects/"+project+"/repositories"
        return self.api_client.request(type_=List[Repository], method="GET", url=url)

class AsyncRepositoryApi(_RepositoryApi):
    pass

class SyncRepositoryApi(_RepositoryApi):
    def save_new_repository(self, repo :  Repository):
        coroutine = self._build_save_new_repository(repo, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def get_company_repositories(self):
        coroutine = self._build_get_company_repositories(server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def load_reposotories_for_project(self, project_name):
        coroutine = self._build_get_all_repositoriesy_for_project(server_config.get_company_name(), project_name)
        return get_event_loop().run_until_complete(coroutine)