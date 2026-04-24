# Architecture

This page describes how KEDEGit is currently structured so contributors can extend the right layer instead of duplicating work across the CLI, orchestration, Git analysis, service, and client packages.

The codebase is organized around a synchronous CLI in `kedehub/__main__.py` that fans out into three main pipelines:

1. ingestion of commits from local repositories into the KEDEHub backend
2. analytics and reporting over already imported commit data
3. cloning or importing repositories from external providers into the local workspace and the server-backed project model

## Layer boundaries

The important boundaries are stable even when individual commands vary:

- CLI layer: `kedehub/__main__.py` defines subcommands, parses arguments, and dispatches handlers with `set_defaults(func=...)`.
- Orchestration layer: `kedehub/kedegit.py` owns repository traversal, commit filtering, diff/stat collection, and the decision about what needs to be persisted.
- Service layer: `kedehub/services/` is mostly thin and translates local actions into backend API calls through `kedehub_client.get_sync_apis()`.
- HTTP client layer: `kedehub_client/` builds the API client, auth middleware, and typed API accessors.
- Configuration layer: YAML app/server config lives in `kedehub/configuration/server_config.py`; per-repository source matching lives in `kedehub/config.py` plus `kedehub/configuration/sources_matcher.py`.
- Git and provider integration layer: `kedehub/gitclient/`, `kedehub/gitcloner/`, and `kedehub/gitupdater/` talk to local Git repositories and external hosting providers.

The CLI should stay thin. If a new feature is fundamentally about repository processing, put it in `KedeGit` or a neighboring module. If it is about remote persistence or retrieval, add or extend a service. If it is about transport, auth, or generated backend bindings, change `kedehub_client/` instead.

## Pipeline 1: Ingestion

The ingestion path is the core flow used by `init-project`, `add-repository`, and `update-projects`.

### Command path

- `init-project` and `add-repository` both dispatch to `add_repository_to_a_project()` in `kedehub/__main__.py`.
- That handler calls `_add_repository(...)`, which constructs `KedeGit(project)` and then calls `KedeGit.add_repository(...)`.
- `update-projects` dispatches to `update_project()`, which constructs `KedeGit(project)` and then calls `KedeGit.update_data()`.

### Orchestration path

`KedeGit` in `kedehub/kedegit.py` owns the ingestion workflow:

- `__init__` loads repositories for a project via `load_reposotories_for_project(...)`.
- `add_repository(...)` ensures the project exists, resolves the per-repo JSON config path, resolves the repository `origin`, stores a repository record through `save_new_repo(...)`, and then processes the local repository.
- `update_data()` iterates the already registered repositories and re-runs processing.
- `_process_repository(...)` loads the last imported commit, walks unprocessed commits with `_iter_unprocessed_commits(...)`, and persists each commit.
- `_create_commit_object(...)` calls `_make_diffed_commit_char_stats(...)` from `kedehub.gitclient.git_utility` to compute lines, chars, and language counts before persisting the result.

### Service and API path

During ingestion, the orchestration layer uses thin services rather than calling the client directly:

- `save_new_repo(...)` in `repository_service.py` calls `get_sync_apis().repository_api.save_new_repository(...)`.
- `assign_new_repo_to_existing_project(...)` and `ensure_project_exists(...)` in `project_service.py` call `project_api` methods.
- `save_new_author(...)` in `author_service.py` calls `author_api.save_new_author(...)`.
- `save_new_commit(...)`, `find_last_commit_for_repository(...)`, and `delete_commits_for_repository(...)` in `commit_service.py` call `commit_api` methods.

That produces the concrete ingestion pipeline below:

`CLI handler -> KedeGit.add_repository()/update_data() -> git log traversal + diff/stat computation -> services/* -> kedehub_client Sync APIs -> HTTP backend`

### Where to extend this pipeline

- Add a new command option in the CLI only if it changes user input or dispatch.
- Add repository-processing rules in `KedeGit` if the behavior changes what commits or stats are produced.
- Add persistence or lookup behavior in `kedehub/services/` if the change is about which backend endpoint is called.
- Add transport or auth behavior in `kedehub_client/` only when the problem is HTTP-facing.

## Pipeline 2: Analytics and Reporting

The analytics and reporting path works on data that has already been imported into the backend.

### Templates and outliers flow

- `templates` dispatches to `do_templates()` in `kedehub/__main__.py`.
- `do_templates()` resolves people with `get_people_to_report_on(...)`.
- `templates find` calls `manage_suspected_templates(...)` in `services/template_finder.py`.
- `manage_suspected_templates(...)` fetches outlier data through `outliers_service.find_outliers(...)`, which calls `get_sync_apis().outliers_api.get_outliers(...)` and converts the JSON payload to a pandas `DataFrame`.
- Interactive confirmation eventually calls `template_service.save_templates(...)`, which posts the selected template commits through `template_api.save_template(...)`.
- `templates update` uses `update_suspected_templates(...)`, which delegates to `outliers_service.update_outliers(...)` and the backend auto-update endpoint.

### KEDE calculation flow

- `stats calculate-kede` dispatches to `calculate_stats()` and then `update_daily_kede(...)`.
- `stats calculate-weekly-kede` dispatches to `calculate_stats()` and then `update_weekly_kede(...)`.
- Both flows iterate people and call `calculate_kede_for_person(...)` or `calculate_weekly_kede_for_person(...)` in `services/kede_service.py`.
- Those functions are thin wrappers over `get_sync_apis().kedestats_api` endpoints.

### Ranklist and summary flow

- `ranklist calculate` dispatches to `calculate_ranklist()` and then `services/ranklist_service.calculate_rank(...)`, which posts to `ranklist_api`.
- `summary` dispatches to `print_summary()`, which renders `summary.table.commit_count_table(...)`.
- `commit_count_table(...)` uses `commit_service.get_project_commits(...)` and formats the result locally with `BeautifulTable`.

### Repair flow adjacent to analytics

The CLI also contains `fix-kede`, which is a repair command, not a primary reporting command. It looks for inconsistent KEDE rows with `find_wrongly_calculated_kede_stats_for_authors_repo_id(...)`, deletes repo KEDE rows, and reruns daily and weekly calculations.

### Where to extend this pipeline

- Add presentation-only output changes in `kedehub/summary/` or the CLI handler.
- Add new backend-backed analytics actions in the service layer first, then wire them into the CLI.
- Keep pandas-based reshaping and interactive template review in `services/template_finder.py`; do not move that logic into the HTTP client.

## Pipeline 3: Cloning and Import

The cloning/import path starts from provider-specific clients and ends with a local clone plus repository registration.

### Provider client stage

Provider integrations live under `kedehub/gitcloner/`:

- `GithubClient.get_repos()` uses PyGithub and returns `clone_url` values.
- `GogsClient.get_repos()` uses `gitea_client` and normalizes clone URLs with `replace_port(...)`.
- `GitlabClient.get_repos()` exists and can enumerate projects, but the current CLI handler that should use it is stubbed.
- `BitbucketClient.get_repos()` exists and can enumerate paginated HTTPS clone URLs, but the current CLI handler that should use it is stubbed.

### Clone and registration stage

- `clone-import-github`, `clone-import-gogs`, and their single-repo variants dispatch to handlers in `kedehub/__main__.py`.
- Those handlers construct `GitCloner(workdir, provider_client)` and call `load_repos()` or `clone_repo(...)`.
- `GitCloner.clone_repo(...)` derives the destination path from the clone URL, skips work if the target path already exists, and also skips when the exact clone URL already appears in the YAML config via `server_config.is_repo_present(...)`.
- After cloning, the handlers call `_add_repository(...)`, which re-enters the ingestion pipeline and registers the repository in the backend and YAML config.

That makes the cloning/import pipeline:

`provider client -> GitCloner -> local clone path -> _add_repository() -> save_new_repo() + YAML repo registration -> commit ingestion`

### Update-local-repos stage

`update-repos` is adjacent to cloning rather than ingestion. It loads company repositories from the backend, enriches them with local paths from YAML config, and then calls `gitupdater.update_repositories(...)` to fetch remotes, inspect local dirtiness, and optionally fast-forward branches after an interactive prompt.

### Current stubbed CLI entries

The parser advertises two clone/import commands whose handlers are currently placeholders:

- `clone-import-gitlab-server` -> `bulk_import_gitlab_server_reps()` -> currently `pass`
- `clone-import-bitbucket-cloud` -> `bulk_import_repos_bitbucket_cloud()` -> currently `pass`

Documenting them as available integrations would be misleading. They are parser-visible but not implemented.

## Command to handler to service map

The table below maps the most important contributor-facing commands to their actual handler and next layer.

| Command | Handler in `kedehub/__main__.py` | Main downstream path |
| --- | --- | --- |
| `init-project` | `add_repository_to_a_project()` | `_add_repository()` -> `KedeGit.add_repository()` -> `project_service.ensure_project_exists()` + `repository_service.save_new_repo()` + `commit_service.save_new_commit()` |
| `add-repository` | `add_repository_to_a_project()` | Same as `init-project`, but for an existing project |
| `update-projects` | `update_project()` | `KedeGit.update_data()` -> `commit_service.find_last_commit_for_repository()` + `commit_service.save_new_commit()` -> optional `calculate_stats_for_authors()` |
| `update-repos` | `update_repos()` | `repository_service.load_company_repositories()` -> `gitupdater.update_repositories()` |
| `templates find|update` | `do_templates()` | `template_finder.manage_suspected_templates()` / `update_suspected_templates()` -> `outliers_service` + `template_service` |
| `stats calculate-kede|calculate-weekly-kede` | `calculate_stats()` | `kede_service.calculate_kede_for_person()` / `calculate_weekly_kede_for_person()` |
| `summary` | `print_summary()` | `summary.table.commit_count_table()` -> `commit_service.get_project_commits()` |
| `ranklist calculate` | `calculate_ranklist()` | `ranklist_service.calculate_rank()` |
| `fix-kede` | `fix_wrongly_calculated_kede()` | `kede_service.find_wrongly_calculated_kede_stats_for_authors_repo_id()` + `delete_kede_for_repo()` + KEDE recalculation |
| `clone-import-github` / `clone-import-gogs` | `bulk_import_github_reps()` / `bulk_import_gogs_reps()` | provider client -> `GitCloner` -> `_bulk_import_reps()` -> `_add_repository()` |
| `clone-import-gitlab-server` / `clone-import-bitbucket-cloud` | `bulk_import_gitlab_server_reps()` / `bulk_import_repos_bitbucket_cloud()` | currently stubbed, no implementation |

## Configuration split

KEDEGit uses two separate configuration models that solve different problems.

### YAML app/server config

`kedehub/configuration/server_config.py` defines `ServerConfiguration`, which loads the application config through Confuse with `confuse.Configuration('KedeGit')`.

This YAML config owns:

- server connection details under `server.protocol`, `server.host`, and `server.port`
- company credentials under `company.name`, `company.user`, and `company.token`
- a local `repos` list used to enrich backend repository records with local paths and per-repo JSON config paths

`kedehub/__init__.py` instantiates `ServerConfiguration()` at import time as `server_config`, so config validation happens very early in process startup.

### Per-repo JSON config

`kedehub/config.py` defines `Configuration`, which reads the per-repository JSON file, usually `kede-config.json`.

That JSON config owns file selection rules such as:

- `sourceFiles`
- `excludedSourceFiles`
- `testFiles`
- `testLineRegex`

`Configuration.is_source_file(...)` delegates glob matching to `kedehub/configuration/sources_matcher.py`, which supports `**` path components and matches Git-style forward-slash patterns against local paths.

### KEDEGITDIR and config discovery

Confuse resolves the YAML config directory for the `KedeGit` app name. In current contributor workflows, `KEDEGITDIR` is the override that points Confuse at an alternate config directory. The onboarding guide covers how to use that override; architecturally, the important point is that the YAML config location is process-global because it is read through the singleton `server_config` object.

### Exact-origin matching for local path enrichment

When repositories are loaded from the backend, KEDEGit enriches them with local `repository_path` and `configuration_file_path` by matching backend records against YAML `repos` entries in `merge_repo_from_db_and_config(...)`.

The match is exact and only compares `origin` strings.

That has two important consequences:

- if the backend stores `https://github.com/org/repo.git` but the YAML file uses an SSH remote like `git@github.com:org/repo.git`, the repo will not be enriched
- if a repo is not enriched, `load_reposotories_for_project(...)` logs that it is missing from local configuration and skips it from the filtered local processing set

If you are debugging why a project loads in the backend but not locally, inspect the exact `origin` string first.

## `kedehub_client` architecture and constraints

`kedehub_client/` is intentionally thin but has a few architectural constraints contributors need to know.

### Client construction

- `get_client()` in `kedehub_client/__init__.py` is `@lru_cache()`-backed and effectively acts as a singleton.
- `get_sync_apis()` and `get_async_apis()` are also cached and expose grouped API accessors.
- The service layer almost always uses `get_sync_apis()`.

### Thin service layer

Most modules in `kedehub/services/` are narrow wrappers that do one of the following:

- forward arguments to a specific API accessor
- convert backend JSON payloads into pandas `DataFrame` objects
- retry around known `UnexpectedResponse` cases with a fixed sleep
- merge local YAML repo metadata into backend repository DTOs

That is why the service layer is the right place for backend-facing business actions, but not for command parsing or HTTP middleware behavior.

### Sync wrappers built on async

The repository is written as a synchronous CLI, but the HTTP client is async underneath:

- `ApiClient.request_sync(...)` in `kedehub_client/api_client.py` uses `get_event_loop().run_until_complete(...)`
- `PasswordFlowClient.request_access_token_sync(...)` and `request_refresh_token_sync(...)` do the same
- generated `Sync*Api` wrappers build on this sync-over-async approach

That is fine for the current CLI model, but it means KEDEGit is not safe to embed unchanged inside an environment that already owns a running event loop, such as some notebooks, GUI runtimes, or async web servers. In those environments, `run_until_complete(...)` can fail with the usual already-running-loop error.

### Auth and failure behavior

Auth is handled by `AuthMiddleware` in `kedehub_client/auth.py`.

The current behavior is:

- the first request can go out without an access token
- a `401` response triggers refresh, then login if refresh is unavailable or fails
- successful login stores tokens in `AuthState`
- a second request is sent with the new access token when login or refresh succeeds

Final failure behavior is process-oriented rather than library-oriented:

- `ApiClient.send(...)` exits the process on a final `401`
- `ApiClient.send_inner(...)` exits the process on `httpx.ConnectError`
- `ServerConfiguration` also calls `sys.exit(...)` for several config validation failures

That behavior is acceptable for the current CLI, but it is a constraint for contributors who want to reuse these modules as an importable library. A library-style embedding would need error propagation instead of process exits.

## Choosing the right layer for a change

- Add or rename commands in `kedehub/__main__.py`.
- Change commit traversal, author construction, or diff/stat collection in `kedehub/kedegit.py` and `kedehub/gitclient/`.
- Change backend operations in `kedehub/services/` first.
- Change auth, request handling, or API accessor construction in `kedehub_client/`.
- Change YAML config semantics in `kedehub/configuration/server_config.py`.
- Change per-repo source matching in `kedehub/config.py` and `kedehub/configuration/sources_matcher.py`.

For more detail on each area, continue with the split subsystem pages under `docs/developer_guide/subsystems/`.