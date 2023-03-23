from asyncio import get_event_loop
from typing import TYPE_CHECKING, Awaitable, List, Dict

from kedehub.services.dro.author_dto import Author
from kedehub_client import server_config

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient


class _AuthorApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_find_all_authors_for_projects(self, project_names: List[str], company: str) -> Awaitable[List[str]]:
        url = '/companies/'+company+'/authors/projects'
        return self.api_client.request(type_= List[str], method="GET",url= url, params = {'project_names': project_names})

    def _build_for_build_author_map(self, project_name, company: str):
        url = '/companies/' + company + '/authors/project'
        return self.api_client.request(type_= Dict[str, Author], method="GET", url=url,
                                       params={'project_name': project_name})

    def _build_find_author_by_cannonical_name_or_aliase(self, name: str):
        url = '/authors/'+name
        return self.api_client.request(type_= Author, method="GET",url=url)


    def _build_for_save_new_author(self, author_name, name, email, company):
        url = '/companies/'+company+'/authors'
        new_author = Author(canonical_name = author_name,
                            name = name,
                            email = email)
        return self.api_client.request(type_= Author, method="POST", url=url, data =new_author.json())

    def _build_update_author_to_user_profile(self, author, company):
        url = '/companies/'+company+'/authors'
        new_author = Author(canonical_name = author.canonical_name,
                            name = "",
                            email = "",
                            user_id = author.user_id)
        return self.api_client.request(type_= int, method="PUT", url=url, data =new_author.json())

class AsyncAuthorApi(_AuthorApi):
    pass


class SyncAuthorApi(_AuthorApi):
    def find_all_authors_for_projects(self, project_names: List[str]):
        coroutine = self._build_for_find_all_authors_for_projects(project_names, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def save_new_author(self, author_name, name, email):
        coroutine = self._build_for_save_new_author(author_name, name, email, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def get_author_by_cannonical_name_or_aliase(self, name):
        coroutine = self._build_find_author_by_cannonical_name_or_aliase(name)
        return get_event_loop().run_until_complete(coroutine)

    def build_author_map(self, project_name: str):
        coroutine = self._build_for_build_author_map(project_name, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def update_author_to_user_profile(self, author):
        coroutine = self._build_update_author_to_user_profile(author, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)