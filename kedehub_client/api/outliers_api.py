from asyncio import get_event_loop
from typing import TYPE_CHECKING

from kedehub.services.dro.author_dto import Author
from kedehub_client import server_config

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient

class _OutliersApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_find_outliers(self, company, person):
        url = "/companies/"+company+"/outliers/persons"
        author = Author(canonical_name = person,
                            name = " ",
                            email = " ")
        return self.api_client.request(type_=str, method="GET", url=url, data = author.json())

    def _build_auto_update_outliers(self, company, person):
        url = "/companies/"+company+"/outliers/persons"
        author = Author(canonical_name = person,
                            name = " ",
                            email = " ")
        return self.api_client.request(type_=str, method="PUT", url=url, data = author.json())

class AsyncOutliersApi(_OutliersApi):
    pass

class SyncOutliersApi(_OutliersApi):
    def get_outliers(self, person):
        """
        """
        coroutine = self._build_find_outliers(server_config.get_company_name(), person)
        return get_event_loop().run_until_complete(coroutine)

    def auto_update_outliers(self, person):
        """
        """
        coroutine = self._build_auto_update_outliers(server_config.get_company_name(), person)
        return get_event_loop().run_until_complete(coroutine)