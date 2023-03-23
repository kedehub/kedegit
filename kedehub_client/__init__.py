from functools import lru_cache
from fastapi.openapi.models import OAuthFlowPassword

from kedehub import server_config
from kedehub_client.api_client import ApiClient, AsyncApis, SyncApis
from kedehub_client.auth import AuthMiddleware, AuthState


class AutoAuthClient(ApiClient):

    def __init__(self, host: str, tokenUrl: str):
        super().__init__(host)
        self.auth_state = AuthState()
        flow = OAuthFlowPassword(tokenUrl=tokenUrl)
        auth_middleware = AuthMiddleware(auth_state=self.auth_state, flow=flow)
        self.add_middleware(auth_middleware)

    def set_creds(self, username: str, password: str) -> None:
        self.auth_state.username = username
        self.auth_state.password = password


# lru_cache is used to (essentially) implement the singleton pattern for accessing the apis
@lru_cache()
def get_client() -> AutoAuthClient:
    server_url = server_config.get_server_url()
    token_url = server_url + '/companies/'+server_config.get_company_name()+'/token'
    client = AutoAuthClient(host = server_url, tokenUrl = token_url)
    client.set_creds(server_config.get_company_user(), server_config.get_user_token())
    return client


@lru_cache()
def get_sync_apis() -> SyncApis[AutoAuthClient]:
    return SyncApis(get_client())


@lru_cache()
def get_async_apis() -> AsyncApis[AutoAuthClient]:
    return AsyncApis(get_client())