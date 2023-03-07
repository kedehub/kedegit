from asyncio import get_event_loop
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient


class _RankListApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_post_calculate_ranklist(self, last_week, today):
        url = "/ranklist/calculate"
        return self.api_client.request(type_= str, method="POST", url=url, json = {
                                                                  "last_week": last_week,
                                                                    "today": today
                                                                })

    def _build_for_load_ranklist(self, people_to_show : str, start_date, end_date):
        url = "/ranklist/persons/"+people_to_show+'?start_date='+str(start_date)
        return self.api_client.request(type_= List[Dict[str, str]], method="GET", url=url)

class AsyncRankListApi(_RankListApi):
    pass

class SyncRankListAApi(_RankListApi):
    def post_calculate_ranklist(self, last_week, today):
        coroutine = self._build_for_post_calculate_ranklist(last_week, today)
        return get_event_loop().run_until_complete(coroutine)

    def load_ranklist(self, people_to_show : str, start_date, end_date):
        coroutine = self._build_for_load_ranklist(people_to_show, start_date, end_date)
        return get_event_loop().run_until_complete(coroutine)