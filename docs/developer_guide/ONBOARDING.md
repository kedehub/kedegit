# Contributor Onboarding

This page covers the supported Phase 1 workflow for running KEDEGit from source.

## Prerequisites

- Python: `setup.py` declares `>=3.8`.
- Recommended Python for development: `3.11`.
- Git: required for local repository inspection and most contributor workflows.
- Linux and Windows contributors may need a local C/C++ build toolchain because `requirements.txt` includes packages with native extensions.

Python 3.11 is the practical recommendation because it is a known-good local baseline for this repository and the pinned dependencies in `requirements.txt` are modern.

## Create a dev environment

From the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell equivalent:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Activation commands by platform:

- macOS and Linux: `source .venv/bin/activate`
- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- Windows Command Prompt: `.venv\\Scripts\\activate.bat`

If you only have Python 3.8, 3.9, or 3.10 available, the declared package metadata still allows it, but 3.11 is the safer contributor baseline.

## Config discovery happens before command handling

KEDEGit loads its server configuration as soon as `kedehub` is imported. In practice that means even this command:

```bash
python -m kedehub --help
```

still requires a valid `config.yaml`.

The config loader is created in `kedehub/__init__.py` and uses `confuse.Configuration('KedeGit')`. The most reliable contributor workflow is to point KEDEGit at a dedicated config directory with `KEDEGITDIR`.

```bash
mkdir -p .kedegit
export KEDEGITDIR="$PWD/.kedegit"
```

Platform variants for `KEDEGITDIR`:

- macOS and Linux: `export KEDEGITDIR="$PWD/.kedegit"`
- Windows PowerShell: `New-Item -ItemType Directory -Force .kedegit | Out-Null; $env:KEDEGITDIR = (Resolve-Path .\\.kedegit)`
- Windows Command Prompt: `set KEDEGITDIR=%CD%\\.kedegit`

If `KEDEGITDIR` is not set, Confuse looks for `config.yaml` in its default `KedeGit` config directory:

- macOS: `~/Library/Application Support/KedeGit/config.yaml`
- Linux: `~/.config/KedeGit/config.yaml`
- Windows: `%APPDATA%\\KedeGit\\config.yaml`

Then create `config.yaml` in that directory:

```yaml
server:
  protocol: https
  host: api.example.invalid
  port: 443

company:
  name: example-company
  user: example-user
  token: example-token
```

Windows-native setup examples:

- PowerShell:

```powershell
New-Item -ItemType Directory -Force .kedegit | Out-Null
$env:KEDEGITDIR = (Resolve-Path .\.kedegit)
@'
server:
  protocol: https
  host: api.example.invalid
  port: 443

company:
  name: example-company
  user: example-user
  token: example-token
'@ | Set-Content -Encoding ascii (Join-Path $env:KEDEGITDIR 'config.yaml')
```

- Command Prompt:

```bat
mkdir .kedegit
set KEDEGITDIR=%CD%\.kedegit
(
  echo server:
  echo   protocol: https
  echo   host: api.example.invalid
  echo   port: 443
  echo.
  echo company:
  echo   name: example-company
  echo   user: example-user
  echo   token: example-token
) > "%KEDEGITDIR%\config.yaml"
```

Notes:

- This example is based on `docs/empty_config.yaml`, but uses non-empty placeholder values so both the early YAML checks and the later Confuse schema checks accept it.
- `api.example.invalid` is intentionally a placeholder. Replace it with a real host, user, and token before running commands that talk to KEDEHub.
- The repository includes `docs/config.yaml` as a Docker-oriented example and `config.yaml` as a local-server example. For first-run contributor setup, prefer the minimal template on this page.

## Run from source

The supported developer workflow is module invocation from the repository checkout:

```bash
python -m kedehub --help
```

That confirms:

- the virtual environment is active
- dependencies import successfully
- the global config file was discovered and validated
- the CLI parser can start

## Offline-safe smoke check

`--help` is the validated first-run smoke check for this repository:

```bash
python -m kedehub --help
```

After that succeeds, the documented safe unit-test subset below is the next recommended offline validation step.

`list-sources` can still be useful when you are debugging repo-specific source matching, but it is not a reliable first-run check on this repository because some local clones can trigger submodule traversal failures.

## Safe local unit-test subset

Start with tests that stay local and avoid the server-backed and network-heavy areas of the suite:

```bash
python -m unittest \
  tests.configuration.test_configfile_format \
  tests.configuration.test_argparser \
  tests.configuration.test_sources_matcher \
  tests.language.test_detect_language \
  tests.utility.test_email_utility \
  tests.utility.test_list_utility \
  tests.gitclient.test_canonical_name \
  tests.gitclient.test_levenshtein_utility
```

This subset is grounded in the current repository and stays away from the areas that depend on a live server, hard-coded local paths, or external Git hosting.

Avoid using `python -m unittest` without arguments as your first check. The full suite includes tests under `tests/integration/`, `tests/kedehub_client/`, `tests/gitcloner/`, plus top-level server-coupled tests such as `tests/kedegit_test.py` and `tests/kedehub_test_load_db_once.py`.

## First-run checklist

1. Activate a virtual environment.
2. Install `requirements.txt`.
3. Set `KEDEGITDIR` to a writable directory.
4. Create a valid `config.yaml` there.
5. Run `python -m kedehub --help`.
6. Run the safe unit-test subset.