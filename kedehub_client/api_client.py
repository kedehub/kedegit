from asyncio import get_event_loop
from functools import lru_cache
from typing import Any, Awaitable, Callable, Dict, Generic, Type, TypeVar, overload
import sys
from httpx import AsyncClient, Request, Response
from pydantic import ValidationError

from .api.commit_api import AsyncCommitApi, SyncCommitApi
from .api.kedestats_api import SyncKedeStatsApi
from .api.outliers_api import AsyncOutliersApi, SyncOutliersApi
from .api.project_api import AsyncProjectApi, SyncProjectApi
from .api.author_api import AsyncAuthorApi, SyncAuthorApi
from .api.ranklist_api import SyncRankListAApi
from .api.repository_api import SyncRepositoryApi
from .api.template_api import SyncTemplateApi
from .api.user_api import SyncUserApi, AsyncUserApi
from .exceptions import ResponseHandlingException, UnexpectedResponse

ClientT = TypeVar("ClientT", bound="ApiClient")


class AsyncApis(Generic[ClientT]):
    def __init__(self, client: ClientT):
        self.client = client

        self.project_api = AsyncProjectApi(self.client)
        self.author_api = AsyncAuthorApi(self.client)
        self.commit_api = AsyncCommitApi(self.client)
        self.ouliers_api = AsyncOutliersApi(self.client)
        self.user_api = AsyncUserApi(self.client)


class SyncApis(Generic[ClientT]):
    def __init__(self, client: ClientT):
        self.client = client

        self.project_api = SyncProjectApi(self.client)
        self.author_api = SyncAuthorApi(self.client)
        self.commit_api = SyncCommitApi(self.client)
        self.outliers_api = SyncOutliersApi(self.client)
        self.template_api = SyncTemplateApi(self.client)
        self.kedestats_api = SyncKedeStatsApi(self.client)
        self.repository_api = SyncRepositoryApi(self.client)
        self.ranklist_api = SyncRankListAApi(self.client)
        self.user_api = SyncUserApi(self.client)

T = TypeVar("T")
Send = Callable[[Request], Awaitable[Response]]
MiddlewareT = Callable[[Request, Send], Awaitable[Response]]


class ApiClient:
    def __init__(self, host: str = None, **kwargs: Any) -> None:
        self.host = host
        self.middleware: MiddlewareT = BaseMiddleware()
        self._async_client = AsyncClient(timeout=None, **kwargs)

    @overload
    async def request(
        self, *, type_: Type[T], method: str, url: str, path_params: Dict[str, Any] = None, **kwargs: Any
    ) -> T:
        ...

    @overload
    async def request(
        self, *, type_: None, method: str, url: str, path_params: Dict[str, Any] = None, **kwargs: Any
    ) -> None:
        ...

    async def request(
        self, *, type_: Any, method: str, url: str, path_params: Dict[str, Any] = None, **kwargs: Any
    ) -> Any:
        if path_params is None:
            path_params = {}
        url = (self.host or "") + url.format(**path_params)
        request = Request(method, url, **kwargs)
        return await self.send(request, type_)

    @overload
    def request_sync(self, *, type_: Type[T], **kwargs: Any) -> T:
        ...

    @overload  # noqa F811
    def request_sync(self, *, type_: None, **kwargs: Any) -> None:
        ...

    def request_sync(self, *, type_: Any, **kwargs: Any) -> Any:  # noqa F811
        """
        This method is not used by the generated apis, but is included for convenience
        """
        return get_event_loop().run_until_complete(self.request(type_=type_, **kwargs))

    async def send(self, request: Request, type_: Type[T]) -> T:
        response = await self.middleware(request, self.send_inner)
        if response.status_code == 200:
            try:
                return parse_as_type(response.json(), type_)
            except ValidationError as e:
                raise ResponseHandlingException(e)
        elif response.status_code == 401:
            print("Authorization failed. Please check your user or token.")
            sys.exit(1)
        else:
            print(f"An unexpected error occurred: {response.status_code} {response.text}")

    async def send_inner(self, request: Request) -> Response:
        try:
            # https://www.python-httpx.org/advanced/#setting-and-disabling-timeouts
            response = await self._async_client.send(request)
        except Exception as e:
            raise ResponseHandlingException(e)
        return response

    def add_middleware(self, middleware: MiddlewareT) -> None:
        current_middleware = self.middleware

        async def new_middleware(request: Request, call_next: Send) -> Response:
            async def inner_send(request: Request) -> Response:
                return await current_middleware(request, call_next)

            return await middleware(request, inner_send)

        self.middleware = new_middleware


class BaseMiddleware:
    async def __call__(self, request: Request, call_next: Send) -> Response:
        return await call_next(request)


@lru_cache(maxsize=None)
def _get_parsing_type(type_: Any, source: str) -> Any:
    from pydantic.main import create_model

    type_name = getattr(type_, "__name__", str(type_))
    return create_model(f"ParsingModel[{type_name}] (for {source})", obj=(type_, ...))


def parse_as_type(obj: Any, type_: Type[T]) -> T:
    if obj is None:
        return None
    model_type = _get_parsing_type(type_, source=parse_as_type.__name__)
    return model_type(obj=obj).obj