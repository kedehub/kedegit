from asyncio import get_event_loop
from typing import TYPE_CHECKING

from kedehub_client import server_config

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient

class _TemplateApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_save_template(self, company, teamplate,  person : str):
        url = "/companies/"+company+"/templates/persons/"+person
        return self.api_client.request(type_=str, method="POST", url=url, data = teamplate)


class AsyncTemplateApi(_TemplateApi):
    pass

class SyncTemplateApi(_TemplateApi):
    def save_template(self, template, person : str):
        """
        """
        coroutine = self._build_save_template(server_config.get_company_name(), template, person)
        return get_event_loop().run_until_complete(coroutine)