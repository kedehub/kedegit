# CLI And Orchestration

This page covers the synchronous command surface in `kedehub/__main__.py` and the repository-processing orchestration in `kedehub/kedegit.py`.

## What lives in the CLI layer

`parse_args(...)` in `kedehub/__main__.py` owns:

- subcommand definitions
- argument parsing
- handler selection through `set_defaults(func=...)`
- only lightweight coordination logic per command

`Main()` parses arguments and calls the selected handler. If no handler is present, it prints a usage reminder instead of raising.

The CLI is synchronous and imperative. There is no command registry abstraction beyond `argparse`.

## Important implemented commands

The most relevant implemented commands for contributors are:

- `init-project`
- `add-repository`
- `update-projects`
- `update-repos`
- `templates`
- `stats`
- `summary`
- `ranklist`
- `bulk-import-repos`
- `clone-import-github`
- `clone-import-gogs`
- `clone-import-github-repo`
- `clone-import-gogs-repo`
- `clone-github-repo`
- `fix-kede`

Two parser-visible commands are currently stubs:

- `clone-import-gitlab-server`
- `clone-import-bitbucket-cloud`

Their handlers exist, but each handler body is just `pass`.

## Command map

| Command | Handler | Orchestration boundary |
| --- | --- | --- |
| `init-project` | `add_repository_to_a_project()` | hands off to `_add_repository()` and then `KedeGit.add_repository()` |
| `add-repository` | `add_repository_to_a_project()` | same flow as `init-project` |
| `update-projects` | `update_project()` | constructs `KedeGit(project)` and calls `update_data()` |
| `update-repos` | `update_repos()` | stays out of `KedeGit`; calls `gitupdater.update_repositories()` |
| `templates` | `do_templates()` | fans out into template and outlier services |
| `stats` | `calculate_stats()` | fans out into daily or weekly KEDE service calls |
| `summary` | `print_summary()` | stays local except for loading project commits |
| `ranklist` | `calculate_ranklist()` | forwards to the ranklist service |

## What lives in `KedeGit`

`KedeGit` is the main ingestion orchestrator. It is the right place for changes that affect how a local Git repository is turned into imported commit records.

The class owns:

- loading repositories for a project in `__init__`
- ensuring a project exists and registering repos in `add_repository(...)`
- iterating over existing repos in `update_data()`
- deleting imported commits in `delete_project_commits()`
- commit traversal in `_iter_unprocessed_commits(...)`
- author caching in `_add_author_if_needed(...)`
- commit DTO creation in `_create_commit_object(...)`
- persistence sequencing inside `_process_repository(...)`

## Ingestion control flow

For `init-project` and `add-repository`, the high-level flow is:

1. `add_repository_to_a_project()` validates that a project name exists.
2. `_add_repository(...)` creates `KedeGit(project)` and normalizes the earliest commit date if provided.
3. `KedeGit.add_repository(...)` ensures the project exists remotely, resolves the repo origin, stores the repository record, adds it to the project, and processes the repo.
4. `_process_repository(...)` walks commits, creates author and commit records, and persists them through services.
5. the CLI optionally triggers `calculate_stats_for_project(...)` after a successful import.

For `update-projects`, the flow is similar but starts from already known repositories and can optionally:

- delete and reclone repository contents when `--temp` is used
- delete existing imported commits when `--clean` is used

## Diff/stat boundary

`KedeGit._create_commit_object(...)` is the main handoff point between Git traversal and metrics extraction. It delegates diff/stat computation to `_make_diffed_commit_char_stats(...)` in `kedehub.gitclient.git_utility`.

If a change affects how added or deleted lines, chars, or language counts are computed, the CLI is the wrong layer. Start in the Git utility path or in `KedeGit`.

## Nearby commands that do not use `KedeGit`

Not every command belongs to the ingestion orchestrator.

- `update-repos` is a local Git maintenance command and goes through `gitupdater`.
- `templates`, `stats`, `ranklist`, and `summary` run on already imported backend data.
- clone/import commands use provider clients and `GitCloner` before they re-enter `_add_repository(...)`.

That split is important when adding a feature: if the feature starts from imported backend data, do not force it through `KedeGit`.