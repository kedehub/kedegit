from typing import TYPE_CHECKING
from asyncio import get_event_loop
from kedehub_client import server_config
from kedehub.services.dro.author_dto import Author

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient

class _KedeStatsApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_post_calculate_kede_for_person(self, company, project, person):
        url = "/companies/"+company + '/projects/'+project+"/person/kedestats/calculate?freq=D"
        author = Author(canonical_name=person,
                        name=" ",
                        email=" ")
        return self.api_client.request(type_= str, method="POST", url=url, data = author.json())

    def _build_for_post_calculate_weekly_kede_for_person(self, company, project, person):
        url = "/companies/"+company+'/projects/'+project+"/person/kedestats/calculate?freq=W"
        author = Author(canonical_name=person,
                        name=" ",
                        email=" ")
        return self.api_client.request(type_= str, method="POST", url=url, data = author.json())

    def _build_get_wrongly_calculated_kede_stats_for_authors_repo_id(self, company, repository_id: int, kede_freq: str):
        url = '/companies/' + company + '/kedestats/wrongly-calculated-kede?repository_id='+str(repository_id)+'&kede_freq='+kede_freq

        return self.api_client.request(type_=str, method="GET", url=url)

    def _build_for_delete_kede_for_repo(self, company, repository_id: int):

        url = "/companies/"+company+"/repositories/"+str(repository_id)+"/kedestats"
        return self.api_client.request(type_= str, method="DELETE", url=url)

class AsyncKedeStatsApi(_KedeStatsApi):
    pass

class SyncKedeStatsApi(_KedeStatsApi):

    def post_calculate_kede_for_person(self, project, person):
        coroutine = self._build_for_post_calculate_kede_for_person(server_config.get_company_name(),project, person)
        return get_event_loop().run_until_complete(coroutine)

    def post_calculate_weekly_kede_for_person(self, project, person):
        coroutine = self._build_for_post_calculate_weekly_kede_for_person(server_config.get_company_name(), project, person)
        return get_event_loop().run_until_complete(coroutine)

    def get_wrongly_calculated_kede_stats_for_authors_repo_id(self, repository_id: int, kede_freq: str):
        """
        """
        coroutine = self._build_get_wrongly_calculated_kede_stats_for_authors_repo_id(server_config.get_company_name(), repository_id, kede_freq)
        return get_event_loop().run_until_complete(coroutine)

    def delete_kede_for_repo(self, repository_id):
        coroutine = self._build_for_delete_kede_for_repo(server_config.get_company_name(),repository_id)
        return get_event_loop().run_until_complete(coroutine)