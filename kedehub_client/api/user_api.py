from asyncio import get_event_loop
from typing import TYPE_CHECKING

from pydantic import EmailStr

from kedehub.services.dro.user_dto import User
from kedehub_client import server_config

if TYPE_CHECKING:
    from kedehub_client.api_client import ApiClient


class _UserApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_create_new_user(self, user, company):
        url = '/users/create/'+company
        return self.api_client.request(type_= User, method="POST", url=url, data =user.json())

    def _build_find_user_by_email(self, email: EmailStr):
        url = '/users'

        return self.api_client.request(type_= User, method="GET", url=url,
                                       params={'email': email})

class AsyncUserApi(_UserApi):
    pass


class SyncUserApi(_UserApi):

    def post_create_new_user(self, user):
        coroutine = self._build_create_new_user(user, server_config.get_company_name())
        return get_event_loop().run_until_complete(coroutine)

    def find_user_by_email(self, email: EmailStr):
        coroutine = self._build_find_user_by_email(email)
        return get_event_loop().run_until_complete(coroutine)

