# HTTP Client And Auth

This page describes the backend transport layer in `kedehub_client/` and the current constraints contributors need to design around.

## Client construction

`kedehub_client/__init__.py` builds a cached client stack:

- `get_client()` creates `AutoAuthClient`
- `get_sync_apis()` returns a cached `SyncApis` bundle
- `get_async_apis()` returns a cached `AsyncApis` bundle

All three functions use `@lru_cache()`, so the process behaves as if it has one shared client and one shared set of API bundles.

`AutoAuthClient` extends `ApiClient`, attaches `AuthMiddleware`, and loads credentials from the YAML config singleton.

## Thin typed API bundles

`SyncApis` and `AsyncApis` group the generated API wrappers by domain.

The synchronous bundle currently exposes accessors such as:

- `project_api`
- `author_api`
- `commit_api`
- `outliers_api`
- `template_api`
- `kedestats_api`
- `repository_api`
- `ranklist_api`
- `user_api`

Most of `kedehub/services/` is built directly on top of these grouped accessors.

## Sync wrappers built on async

Although the CLI is synchronous, the client transport is async underneath.

Two explicit examples in the repository are:

- `ApiClient.request_sync(...)` uses `get_event_loop().run_until_complete(...)`
- `PasswordFlowClient.request_access_token_sync(...)` and `request_refresh_token_sync(...)` do the same

The generated synchronous API wrappers follow the same overall sync-over-async model. That is acceptable for a command-line process that owns the event loop, but it is a real constraint when embedding the code elsewhere.

## Already-running-event-loop caveat

If KEDEGit is imported into an environment that already has a running event loop, `run_until_complete(...)` can fail.

Typical risky environments include:

- notebooks
- GUI applications
- async web apps
- test harnesses that already manage an event loop

The current repository is designed first for synchronous CLI execution, not for async-native library reuse.

## Request and response behavior

`ApiClient.request(...)` builds an `httpx.Request`, sends it through middleware, and parses successful JSON responses into typed models.

Current status handling is process-oriented:

- `200` returns parsed data
- `401` prints an authorization message and exits the process
- other non-`200` statuses print an unexpected error message
- `httpx.ConnectError` prints a connection error and exits the process

This is important when deciding whether to extend the service layer or the client layer. If the problem is better error propagation, the change belongs in `kedehub_client`, not in the CLI handlers.

## Auth flow

`AuthMiddleware` in `kedehub_client/auth.py` handles the current login lifecycle.

The flow is:

1. if cached tokens are close to expiry, try refresh before sending the request
2. if an access token is already available, add it to the outgoing request
3. send the request
4. if the response is not `401`, return it
5. on `401`, try refresh; if that fails, try password-flow login
6. if login or refresh succeeds, resend the request with the new access token
7. if auth still fails, return the `401` response to `ApiClient.send(...)`, which exits the process

The first request may therefore be unauthenticated and only trigger login after the backend challenges it.

## Credential source

The username and password are loaded from the YAML config singleton through:

- `server_config.get_company_user()`
- `server_config.get_user_token()`

The token endpoint is derived from the configured server URL and company name:

`<server_url>/companies/<company_name>/token`

## Contributor implications

- Put backend endpoint wiring and transport fixes in `kedehub_client/`.
- Put backend business operations in `kedehub/services/`.
- Expect process exits today for final auth or connection failures.
- Treat async embedding as unsupported without refactoring the sync-over-async boundary.