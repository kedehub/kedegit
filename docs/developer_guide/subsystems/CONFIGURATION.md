# Configuration

KEDEGit uses two separate configuration models:

- a process-wide YAML config for server connection details, credentials, and the local repository registry
- a per-repository JSON config for source-file and test-file matching

Contributors should keep these concerns separate. They solve different problems and are loaded by different modules.

## YAML app and server config

`kedehub/configuration/server_config.py` defines `ServerConfiguration` and validates a Confuse-backed YAML file for the `KedeGit` application name.

The required YAML keys are:

- `server.protocol`
- `server.host`
- `server.port`
- `company.name`
- `company.user`
- `company.token`

The YAML file can also include:

- `repos`, a sequence of objects with `origin`, `repository_path`, and `configuration_file_path`

`ServerConfiguration` provides getters such as:

- `get_server_url()`
- `get_company_name()`
- `get_company_user()`
- `get_user_token()`
- `get_repos()`
- `add_new_repo(...)`

## Import-time behavior

`kedehub/__init__.py` creates a module-level singleton:

`server_config = ServerConfiguration()`

That means YAML discovery and validation happen at import time, before most commands reach their main logic. This is why startup failures for missing files, malformed YAML, or missing required keys happen early and terminate the process.

## KEDEGITDIR behavior

Confuse determines where the `KedeGit` YAML config lives. In contributor workflows, `KEDEGITDIR` is the environment override used to point KEDEGit at a different config directory.

Architecturally, that means:

- the resolved config directory is global for the process
- imports that touch `kedehub` can observe the override immediately
- tests and scripts that need a temporary config must set `KEDEGITDIR` before importing modules that transitively import `kedehub`

## YAML validation constraints

`validate_yaml_file(...)` in `ServerConfiguration` is strict.

It currently rejects:

- missing files
- invalid YAML syntax
- missing required keys
- UTF-8 BOM-prefixed files
- any file containing non-ASCII bytes

That strictness is part of current behavior and explains why some startup failures call `sys.exit(...)` before any network request is made.

## Repository registry in YAML

The YAML `repos` list is not just documentation. It is the local registry that ties backend repository records to local clone paths and to per-repo JSON config paths.

When a new repo is added through `repository_service.save_new_repo(...)`, the code also calls `server_config.add_new_repo(...)` to append the repo metadata to the YAML file.

Each repo entry contains:

- `origin`
- `repository_path`
- `configuration_file_path`

## Exact-origin matching for enrichment

When repositories are loaded from the backend, KEDEGit enriches the DTOs with local fields by calling `merge_repo_from_db_and_config(...)` in `kedehub/services/__init__.py`.

The logic is simple and strict: a backend repository record is enriched only when `repo_from_db.origin == repo_data_from_config['origin']`.

This exact string match means the following will not match each other:

- HTTPS and SSH remotes for the same repository
- clone URLs with and without `.git`
- provider URLs rewritten through a proxy or alternate hostname

If enrichment fails:

- `load_reposotories_for_project(...)` logs that the repository is not in the local configuration file
- that repo is skipped from the filtered list used for local ingestion work

This is the first thing to verify when a repository exists in the backend but local commands cannot process it.

## Per-repository JSON config

`kedehub/config.py` defines `Configuration`, which loads a repository-local JSON file, commonly `kede-config.json`.

This JSON config controls file classification rather than server access.

Supported keys include:

- `sourceFiles`
- `excludedSourceFiles`
- `testFiles`
- `testLineRegex`

The JSON file is optional. Missing files are treated as an empty config.

## Source matching rules

`Configuration.is_source_file(...)` combines include and exclude patterns.

Pattern evaluation is delegated to `kedehub/configuration/sources_matcher.py`, which:

- supports `*` and `?` within a single path component
- supports `**` as a whole path component spanning multiple directories
- normalizes both `/` and `\` in file paths
- raises a `ValueError` if `**` is used incorrectly inside a larger path component

This matcher is used by `iter_sources(...)` and by diff/stat processing to decide which files count as source.

## Choosing the right config to extend

- Add server URL, company identity, or local repo registry behavior in the YAML config path.
- Add file inclusion, exclusion, or test matching behavior in the JSON config path.
- Do not put repository-local file rules into the YAML config unless you are intentionally changing the architecture.