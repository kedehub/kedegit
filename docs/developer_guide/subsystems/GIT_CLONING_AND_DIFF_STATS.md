# Git Cloning And Diff Stats

This subsystem covers two related but separate concerns:

- talking to local Git repositories to compute ingestion data
- talking to hosting providers and cloning repositories into the local workspace

They meet when a freshly cloned repository is handed back into `_add_repository(...)` and processed by `KedeGit`.

## Local Git analysis

The local Git analysis path is centered in `kedehub/kedegit.py` and `kedehub/gitclient/git_utility.py`.

The main steps are:

1. resolve a `git.Repo` object for the local repository
2. walk commit hashes with `git log --all --reverse --date-order --format='%H'`
3. skip commits that were already imported or are older than the last imported commit boundary
4. compute parent relationships
5. compute added and deleted lines, chars, and language counts through `_make_diffed_commit_char_stats(...)`
6. persist author and commit DTOs through the service layer

This is the boundary to change if a feature affects what gets counted from Git history.

## Local repo maintenance

`update-repos` is implemented in `kedehub/gitupdater/gitupdater.py`.

That module is intentionally separate from ingestion because it is about working copies, branches, and fetch state, not about commit import.

The current flow:

- prompts the user for whether branches should be fast-forwarded
- fetches remotes for each configured repository
- reports local dirty and untracked files
- lists branch ahead/behind state relative to the default branch
- optionally runs `git pull origin <branch> --ff-only`

This command is interactive and does not call `KedeGit`.

## Provider clients

Provider integrations live in `kedehub/gitcloner/`.

- `GithubClient` uses PyGithub and returns GitHub clone URLs for an organization.
- `GogsClient` uses `gitea_client` and rewrites clone URLs to drop the parsed port in `replace_port(...)`.
- `GitlabClient` can enumerate GitLab project clone URLs but is not wired to a working CLI command today.
- `BitbucketClient` can enumerate paginated HTTPS clone URLs but is not wired to a working CLI command today.

The provider client boundary is the right place to change remote enumeration logic, tokens, or provider-specific URL normalization.

## `GitCloner`

`GitCloner` in `kedehub/gitcloner/git_cloner.py` turns provider results into local clones.

It owns:

- loading clone URLs from a provider client with `load_repos()`
- deriving a repository folder name from the clone URL
- choosing a clone destination under the requested working directory
- skipping clones when the target path already exists locally
- skipping clones when the exact clone URL already exists in YAML config through `server_config.is_repo_present(...)`
- delegating actual clone work to `clone_a_repo(...)`

`clone_a_repo(...)` is a thin wrapper over `Repo.clone_from(...)` with progress logging.

## Import after clone

Clone commands do not stop at fetching a working copy. The successful clone path usually continues with:

1. `GitCloner.clone_repo(...)`
2. `_add_repository(...)`
3. `KedeGit.add_repository(...)`
4. repository save to the backend and YAML config
5. commit ingestion
6. optional analytics recalculation

That split matters when a bug appears after cloning. Failures before `_add_repository(...)` belong to the provider or clone layer. Failures after that point belong to ingestion or backend communication.

## Current command coverage

Implemented clone/import commands:

- `clone-import-github`
- `clone-import-gogs`
- `clone-import-github-repo`
- `clone-import-gogs-repo`
- `clone-github-repo`
- `bulk-import-repos` for importing already cloned local directories

Parser-visible but currently unimplemented commands:

- `clone-import-gitlab-server`
- `clone-import-bitbucket-cloud`

Do not describe GitLab server or Bitbucket cloud import as supported end-to-end until those handlers do real work.