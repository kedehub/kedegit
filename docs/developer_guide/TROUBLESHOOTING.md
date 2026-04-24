# Troubleshooting

This page covers the startup failures that contributors are most likely to hit during local setup.

## `config.yaml` is missing

Symptom:

- `python -m kedehub --help` exits immediately.
- The error mentions a missing YAML file.

Cause:

- `kedehub/__init__.py` creates `ServerConfiguration()` at import time.
- Because of that, command parsing never starts unless the global config file is present and valid.

What to do:

```bash
mkdir -p .kedegit
export KEDEGITDIR="$PWD/.kedegit"
cat > "$KEDEGITDIR/config.yaml" <<'EOF'
server:
  protocol: https
  host: api.example.invalid
  port: 443

company:
  name: example-company
  user: example-user
  token: example-token
EOF
```

Windows equivalents:

- PowerShell: `$env:KEDEGITDIR = (Resolve-Path .\\.kedegit)`
- Command Prompt: `set KEDEGITDIR=%CD%\\.kedegit`

If you are creating the directory from scratch on Windows, use `New-Item -ItemType Directory -Force .kedegit` in PowerShell or `mkdir .kedegit` in Command Prompt before writing `config.yaml`.

Then rerun:

```bash
python -m kedehub --help
```

## YAML validation fails before the CLI starts

Symptom:

- startup fails before your subcommand runs
- errors mention YAML validation, missing keys, formatting, BOM, or non-ASCII characters

Cause:

- `ServerConfiguration.validate_yaml_file()` checks required keys before loading the config
- it rejects files with a UTF-8 BOM
- it rejects files containing non-ASCII characters

What to do:

- Keep the file ASCII-only.
- Save it as plain UTF-8 without BOM, using only ASCII characters in the content.
- Make sure these keys are present and non-empty enough to parse cleanly:
  - `server.protocol`
  - `server.host`
  - `server.port`
  - `company.name`
  - `company.user`
  - `company.token`
- If you copied a sample from elsewhere, rewrite it using the minimal example from [ONBOARDING.md](./ONBOARDING.md).

If a file looks correct but still fails, recreate it from scratch in a plain-text editor instead of reusing a document that may have hidden characters.

## Server-backed commands exit with `401`

Symptom:

- commands that talk to KEDEHub print `Authorization failed. Please check your user or token.` and exit

Cause:

- `kedehub_client/api_client.py` exits on HTTP `401`
- placeholder onboarding values are enough for `--help`, but not for server-backed commands

What to do:

- replace `company.user` and `company.token` with real values
- verify `company.name` matches the company on the target server
- rerun a server-backed command only after `python -m kedehub --help` and the safe unit-test subset succeed

## Server-backed commands exit with a connection error

Symptom:

- commands print `Connection error: ...` and terminate

Cause:

- `kedehub_client/api_client.py` exits on `httpx.ConnectError`
- the configured host is unreachable, incorrect, or intentionally offline

What to do:

- check `server.protocol`, `server.host`, and `server.port`
- confirm the target service is reachable from your machine
- for initial setup, stay with offline-safe commands such as `python -m kedehub --help` and the safe unit-test subset from [ONBOARDING.md](./ONBOARDING.md)

## A repo exists locally, but KEDEGit says it is not in local configuration

Symptom:

- server-backed repository commands report that a repository is not in the local configuration file
- you know the repository is cloned locally

Cause:

- local path mapping is restored by exact `origin` string match between server data and `config.yaml`
- a local clone using SSH and a config entry using HTTPS are different strings
- renamed remotes or changed `origin` URLs can cause the same mismatch

What to do:

- compare the clone's current remote with the config entry:

```bash
git -C /absolute/path/to/local/repo remote get-url origin
```

- make sure the `repos` entry in `config.yaml` uses the exact same `origin` value
- if needed, update the clone remote or the config entry so they match exactly

Example `repos` entry:

```yaml
repos:
  - origin: https://github.com/example-org/example-repo.git
    repository_path: /absolute/path/to/local/repo
    configuration_file_path: /absolute/path/to/local/repo/kede-config.json
```

## `list-sources` fails on a local repository

Symptom:

- `python -m kedehub list-sources /path/to/repo` fails even though the global config is valid

Common causes:

- the path is not a Git repository
- the repo-specific `kede-config.json` path is wrong
- Git is not installed or not available in the active environment
- the repository contains submodule layouts that trigger the current traversal bug in `iter_sources`

What to do:

- verify the repository opens with Git locally
- if you pass `-c`, confirm that file exists
- treat `list-sources` as a repo-debugging command instead of a first-run smoke test
- fall back to `python -m kedehub --help` plus the safe unit-test subset while diagnosing the local repo layout