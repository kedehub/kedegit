# Testing Guide

This repository mixes offline-safe tests with tests that assume a running backend service, a separate local checkout, or external network access. Use a narrow default workflow first, then opt into heavier areas deliberately.

## One rule before any `kedehub` import

Set `KEDEGITDIR` before importing modules that depend on `kedehub` startup.

`kedehub/__init__.py` creates `ServerConfiguration()` at import time, so config discovery and YAML validation happen immediately. If `KEDEGITDIR` is missing or points at an invalid config directory, tests can fail during import rather than during the actual assertion path.

Safe setup from the repository root:

```bash
mkdir -p .kedegit-test
cp tests/data/empty_config.yaml .kedegit-test/config.yaml
export KEDEGITDIR="$PWD/.kedegit-test"
```

## Default workflow: offline-safe tests

These areas are the safer default for contributor changes that do not need a backend service or real network activity:

- `tests/configuration/test_argparser.py`
- `tests/configuration/test_kedegit_config.py`
- `tests/configuration/test_configfile_format.py`
- `tests/configuration/test_sources_matcher.py`
- `tests/language/test_detect_language.py`
- `tests/utility/test_email_utility.py`
- `tests/utility/test_list_utility.py`
- `tests/gitclient/test_canonical_name.py`
- `tests/gitclient/test_levenshtein_utility.py`

Run a safe subset:

```bash
export KEDEGITDIR="$PWD/.kedegit-test"
python -m unittest \
  tests.configuration.test_argparser \
  tests.configuration.test_kedegit_config \
  tests.configuration.test_configfile_format \
  tests.configuration.test_sources_matcher \
  tests.language.test_detect_language \
  tests.utility.test_email_utility \
  tests.utility.test_list_utility \
  tests.gitclient.test_canonical_name \
  tests.gitclient.test_levenshtein_utility
```

For a CLI-only feature such as the documented `config-info` recipe, start smaller:

```bash
export KEDEGITDIR="$PWD/.kedegit-test"
python -m unittest tests.configuration.test_argparser
```

Then run the command locally after your change:

```bash
export KEDEGITDIR="$PWD/.kedegit-test"
python -m kedehub config-info
```

That last command is a recipe validation step for a feature you add locally. It is not expected to work on the current repository state because `config-info` is not implemented yet.

## Opt-in and heavier test areas

These areas are real parts of the repository, but they are not safe default checks for everyday edits.

### Top-level server-coupled tests

- `tests/kedegit_test.py`
- `tests/kedehub_test_load_db_once.py`

These tests start a separate `kedehub_server` checkout from hard-coded machine-specific paths under `/Users/dimitarbakardzhiev/git/kedehub_server/...`. Treat them as environment-coupled.

### Integration flows

- `tests/integration`

These tests exercise heavier end-to-end repository processing behavior. They are useful once you are intentionally validating ingestion flows, not when you are only changing parser wiring or config reporting.

### Backend API client tests

- `tests/kedehub_client/api`

These tests are coupled to API behavior and are not a safe first pass for offline contributor work.

### Clone and provider tests

- `tests/gitcloner`

These tests sit closer to real clone workflows and provider-specific interactions. Expect more environmental assumptions here than in the configuration or small utility tests.

## How to choose the right test scope

- If you changed argparse wiring or config-only output, run one or two targeted `tests/configuration/...` modules.
- If you changed source-file classification, add `tests/gitclient/test_config.py` or `tests/configuration/test_sources_matcher.py` as needed.
- If you changed anything that talks to services, APIs, or cloning workflows, treat the heavier areas as opt-in and document what environment you used.

Avoid using `python -m unittest` with no module selection as your first check. The repository contains enough environment-coupled coverage that a full run is not an honest default workflow.

## Current repo state to keep in mind

- Import order matters because configuration is created at import time.
- Some tests intentionally expect startup failures such as invalid YAML, missing keys, or BOM/non-ASCII input.
- The safest contributor loop is: set `KEDEGITDIR`, run one narrow test module, then run the local CLI command you changed.