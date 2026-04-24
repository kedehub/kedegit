# Services Layer

The service modules in `kedehub/services/` are deliberately thin. They are the boundary between orchestration code and the typed HTTP client bundle from `kedehub_client`.

## What the services layer does

Most service modules do one or more of the following:

- call one method on `get_sync_apis()`
- convert backend JSON payloads into pandas `DataFrame` objects
- add small retry behavior around `UnexpectedResponse`
- combine backend DTOs with local YAML metadata

This layer is intentionally not where CLI parsing, auth middleware, or low-level Git traversal should live.

## Core ingestion-facing services

These services are on the hot path for repository import and update:

- `author_service.py`: create and load author records
- `commit_service.py`: create, fetch, and delete commit records
- `project_service.py`: ensure a project exists and attach repositories to it
- `repository_service.py`: save repositories and load repository DTOs

`repository_service.load_reposotories_for_project(...)` is especially important because it merges backend data with the local YAML repo registry and filters out repos that do not have a local path match.

## Analytics-facing services

These modules support analytics and reporting commands:

- `kede_service.py`: daily and weekly KEDE calculations, KEDE repair helpers
- `outliers_service.py`: fetch outlier datasets and trigger backend outlier updates
- `template_service.py`: save template commit selections
- `ranklist_service.py`: trigger ranklist calculation

These modules are intentionally thin. The heavier pandas reshaping and interactive prompting for templates lives one layer up in `template_finder.py`.

## Summary and local formatting

Not every read path is a service call plus direct print.

For example, `summary.table.commit_count_table(...)` pulls commit DTOs through `commit_service.get_project_commits(...)` and formats the summary locally with `BeautifulTable`.

That is a good pattern when the backend already provides the raw data and the CLI only needs a different local presentation.

## Repo enrichment helper

`kedehub/services/__init__.py` currently exposes `merge_repo_from_db_and_config(...)`.

This helper is part of the service-layer boundary because it merges two data sources:

- repository DTOs loaded from the backend
- local repo metadata loaded from the YAML config

The merge key is an exact `origin` string match.

## When to add a new service

Add or extend a service when:

- the CLI needs a new backend operation
- multiple commands need the same backend action
- a backend response needs consistent local conversion or retry behavior

Do not add a service just to wrap local formatting or command parsing.

## Current constraints to keep in mind

- services generally assume the synchronous API bundle from `get_sync_apis()`
- several services catch `UnexpectedResponse` and sleep for 35 seconds instead of surfacing a structured error
- service modules are not a full domain layer; many are thin facades over generated API methods

That design is fine for the current CLI-first repository, but contributors should not expect rich business invariants to be centralized here.