# Contributing Workflow

This page is the Phase 6 contributor recipe: make one small, offline-safe change, test it locally, and stop before you need a running KEDEHub server or real network access.

The example feature is deliberately a documentation recipe, not a statement about the current CLI. The command described below does not exist in the repository today.

## Goal

Add a new CLI subcommand named `config-info` that prints:

- the resolved KEDEGit config directory
- the resolved server URL
- whether the YAML config has a `repos` list and, if so, how many entries it contains

This is a good first change because it stays in the CLI and configuration layer, and it can be validated locally with a temporary config directory.

## Before you edit code

Set `KEDEGITDIR` before you import any module that depends on `kedehub` startup behavior.

`kedehub/__init__.py` instantiates `ServerConfiguration()` at import time. That means configuration lookup and YAML validation happen as soon as Python imports `kedehub`, before CLI dispatch reaches your new handler.

Safe shell setup from the repository root:

```bash
mkdir -p .kedegit-dev
cp tests/data/empty_config.yaml .kedegit-dev/config.yaml
export KEDEGITDIR="$PWD/.kedegit-dev"
```

For tests, the same rule applies more strictly: set `KEDEGITDIR` before importing `kedehub`-dependent modules. Existing tests already reflect that pattern in places such as `tests/__init__.py` and `tests/configuration/test_kedegit_config.py`.

## Code points to change

### 1. Add the handler in `kedehub/__main__.py`

Add a new handler function near the other CLI handlers:

```python
def config_info(_options):
    ...
```

The handler should read from the existing configuration object or from `ServerConfiguration`, then print a small, stable output format. Keep it simple enough that a stdout-based unit test can assert on it.

### 2. Wire the parser in `kedehub/__main__.py`

In `parse_args(...)`, add a subparser:

```python
config_info_parser = command_parsers.add_parser(
    'config-info',
    help='Print resolved configuration information'
)
config_info_parser.set_defaults(func=config_info)
```

This follows the current pattern used by commands such as `list-projects`, `summary`, and `fix-kede`.

### 3. Add a configuration accessor only if you need one

`kedehub/configuration/server_config.py` already exposes the core accessors you need for this recipe:

- `get_config_dir()`
- `get_server_url()`
- `get_repos()`

If your output format needs anything else, add one small accessor in `server_config.py` rather than reaching into Confuse internals from multiple call sites. Follow the current style: keep access centralized in `ServerConfiguration`.

## Suggested implementation shape

One low-risk approach is:

1. Read the config directory with `get_config_dir()`.
2. Read the server URL with `get_server_url()`.
3. Read repos defensively:
   - `get_repos()` exits if `repos` is missing.
   - if you want `config-info` to report `repos: absent` instead of exiting, add a small accessor in `server_config.py` that returns `None` or `[]` safely for this command.

That tradeoff is the main implementation decision in this recipe. The current repository behavior is strict about missing `repos`, so the guide should not pretend otherwise.

## Tests to add

Keep the test coverage local and narrow.

### Parser test

Extend `tests/configuration/test_argparser.py` with a case that proves the new subcommand is wired:

```python
args = self._parse('config-info')
self.assertEqual('config-info', args.subparser_name)
self.assertEqual(config_info, args.func)
```

That is the cheapest test that confirms the argparse wiring in `kedehub/__main__.py`.

### Output test

Add one focused test for the handler output. A practical location is a new configuration-oriented test module under `tests/configuration/`, because the behavior is mostly CLI plus config formatting.

The test should:

1. create or reuse an isolated config directory
2. set `KEDEGITDIR` before importing the code under test
3. provide a minimal YAML fixture
4. patch `print` or capture stdout
5. assert on stable fragments such as the config directory, server URL, and repo count

If you use a fixture with a `repos` section, the command can stay entirely offline.

## Local validation after the change

After implementing `config-info`, validate it in this order.

### 1. Run the narrow parser test

```bash
export KEDEGITDIR="$PWD/.kedegit-dev"
python -m unittest tests.configuration.test_argparser
```

This is the cheapest check for the new command wiring.

### 2. Run the handler-focused test

```bash
export KEDEGITDIR="$PWD/.kedegit-dev"
python -m unittest tests.configuration.test_config_info
```

Use whatever test module name you actually add. The important part is to keep the command scoped to the new feature rather than expanding to the full suite.

### 3. Run the CLI command directly

```bash
export KEDEGITDIR="$PWD/.kedegit-dev"
python -m kedehub config-info
```

Because `KEDEGITDIR` is set first, import-time configuration should resolve from your temporary local directory instead of the user-level default path.

## What not to do for a first contribution

- Do not start with the top-level tests `tests/kedegit_test.py` or `tests/kedehub_test_load_db_once.py`; they start an external `kedehub_server` checkout via machine-specific paths.
- Do not start with `tests/integration`; those tests exercise repo processing flows that are much heavier than this CLI change.
- Do not start with `tests/kedehub_client/api`; those tests are coupled to backend API behavior.
- Do not start with `tests/gitcloner`; those tests move closer to real hosting providers and clone workflows.

Use [TESTING.md](./TESTING.md) as the source of truth for which test areas are safe by default and which ones are opt-in.