from asyncio import get_event_loop
from typing import TYPE_CHECKING, List, Optional

from kedehub.services.dro.commit_dto import Commit
from kedehub_client import server_config

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient

class _CommitApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_get_commits_per_project(self, project_name, company: str):
        url = '/companies/' + company + '/commits/projects/' + project_name
        return self.api_client.request(type_= List[Commit], method="GET", url=url)

    def _build_store_new_commit(self, commit_dto, company: str):
        url = '/companies/' + company + "/commits"
        return self.api_client.request(type_= Commit, method="POST", url=url, data =commit_dto.json())

    def _build_get_commits_per_company(self, company: str):
        url = '/companies/' + company + '/commits'
        return self.api_client.request(type_= List[Commit], method="GET", url=url)

    def _build_get_last_commit_for_repository(self, company, repository_id):
        url = '/companies/' + company + '/commits/repositories/' + str(repository_id) + '?filter=last'
        return self.api_client.request(type_= Optional[Commit] , method="GET", url=url)

    def _build_delete_repository_commits(self, company, repository_id):
        url = '/companies/' + company + '/commits/repositories/' + str(repository_id)
        return self.api_client.request(type_= int , method="DELETE", url=url)

class AsyncCommitApi(_CommitApi):
    pass

class SyncCommitApi(_CommitApi):

    def find_commits_per_project(self, project_name):
        coroutine = self._build_get_commits_per_project(project_name, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def store_new_commit(self, commit_dto):
        coroutine = self._build_store_new_commit(commit_dto, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def get_commits_per_comoany(self):
        coroutine = self._build_get_commits_per_company(server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def find_last_commit_for_repository(self, repository_id):
        coroutine = self._build_get_last_commit_for_repository(server_config.get_company_name(), repository_id)
        return get_event_loop().run_until_complete(coroutine)

    def delete_repository_commits(self, repository_id):
        coroutine = self._build_delete_repository_commits(server_config.get_company_name(), repository_id)
        return get_event_loop().run_until_complete(coroutine)