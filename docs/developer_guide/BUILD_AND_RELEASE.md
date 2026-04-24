# Build and Release

This page covers the current contributor-facing build and distribution paths for KEDEGit.

The supported contributor workflow is still run-from-source from a repository checkout:

```bash
python -m pip install -r requirements.txt
python -m kedehub --help
```

Use the other paths on this page as maintainer or experimentation workflows. They are not currently as portable as the run-from-source path.

## Supported path: run from source

Run from the repository root inside an activated virtual environment:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m kedehub --help
```

Why this is the supported path:

- `requirements.txt` is the only dependency list in this repository that matches the current runtime surface.
- Existing docs such as `docs/howto.md` and `docs/installation_hoto.txt` already use `python -m kedehub` from a checkout.
- `kedehub/__main__.py` is the CLI entrypoint the repository actually runs and packages.
- This path avoids depending on incomplete packaging metadata.

Keep in mind that `kedehub/__init__.py` loads server configuration at import time, so even `python -m kedehub --help` still needs a valid `config.yaml`. See [ONBOARDING.md](./ONBOARDING.md) for the current first-run setup.

## Pip install and editable install caveats

`setup.py` exists, but it is not enough by itself for contributor setup.

Current limitations:

- `setup.py` underdeclares runtime dependencies compared to `requirements.txt`.
- There is no `console_scripts` entry point, so installation does not create a `kedegit` or `kedehub` shell command.
- The current docs and code paths assume module execution with `python -m kedehub`, not a generated console script.

Today `setup.py` declares only these runtime dependencies:

- `gitpython`
- `python-dateutil`
- `beautifultable`

By contrast, `requirements.txt` also includes packages that the current codebase relies on directly or indirectly, including `confuse`, `PyYAML`, `tqdm`, `requests`, `httpx`, `unidiff`, `pandas`, `numpy`, `Levenshtein`, and others.

That means this command is not sufficient on its own:

```bash
python -m pip install .
```

This command is also not sufficient on its own:

```bash
python -m pip install -e .
```

Treat both install modes as limited packaging paths under the current `setup.py` state. If you use either one for local import convenience, treat it as an add-on to the supported workflow, not a replacement for it:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m kedehub --help
```

Even in that form, the supported invocation remains `python -m kedehub`.

## PyInstaller

The intended PyInstaller entrypoint is `kedehub/__main__.py`.

The repository includes two spec files:

- `kedegit.spec`: the current spec file.
- `old_kedegit.spec`: an older variant that adds hidden imports such as `unidiff`, `git`, `gitdb`, `mmap`, `smmap`, and `multiprocessing`.

These files are useful as local build history, but they are not currently portable release assets.

### Current portability issues

`kedegit.spec` and `old_kedegit.spec` both hard-code assumptions about one maintainer environment:

- They point at an absolute source path for `kedehub/__main__.py`.
- They use a venv-specific `pathex` entry under `./venv311/lib/python3.11/site-packages/`.
- `kedegit.spec` currently sets `upx=True`, so successful compression depends on UPX being installed and working on the build host. That adds another machine-specific portability dependency.
- They assume local dependencies have already been installed into that exact environment.
- They do not document or encode platform-specific hidden-import handling in a reusable way.

`docs/installation_hoto.txt` shows the same pattern in command form: local absolute paths, virtual-environment-specific `--paths` values, and separate commands per machine or platform.

### What works today

PyInstaller can still be used locally by a maintainer who adapts the spec or command line to the machine that is doing the build.

Examples already present in the repository:

- direct `pyinstaller --onefile ... kedehub/__main__.py` commands in `docs/installation_hoto.txt`
- `pyinstaller ~/git/kedegit/kedegit.spec` for a local macOS setup

Treat those as machine-local recipes, not portable release instructions.

### Maintainer checklist for a portable spec

Before treating the spec as a release artifact, update it so it no longer depends on one workstation:

1. Replace the absolute script path with a repository-relative path to `kedehub/__main__.py`.
2. Remove hard-coded `venv311` `pathex` assumptions and prefer a build environment that resolves installed dependencies normally.
3. Re-check hidden imports against the current runtime surface. `old_kedegit.spec` is useful context here because it documents previous import-discovery gaps.
4. Verify whether data files or non-code assets need to be collected explicitly.
5. Build from a clean environment and confirm the binary starts with only the packaged contents available.
6. Smoke-test the binary with a real `config.yaml`, because startup configuration loading happens during import.
7. Record a reproducible build command in this guide once the spec is portable.

Until that checklist is done, describe PyInstaller as a local maintainer workflow rather than a supported portable distribution path.

## Docker

The repository also includes a Docker build and run path.

- Use [DOCKER.md](./DOCKER.md) for the current container workflow, required build context, config mount path, and known limitations.
- Under the current Dockerfile, treat Docker as a contributor or maintainer aid rather than the primary supported development path.

## Release guidance

This repository does not currently provide one clean, portable release pipeline for contributors.

For now:

- Use run-from-source for contributor setup and everyday development.
- Treat both `pip install .` and `pip install -e .` as incomplete paths unless you also install from `requirements.txt`.
- Use editable install only together with `requirements.txt`, and still run with `python -m kedehub`.
- Use PyInstaller only as a maintainer-managed workflow that needs environment-specific validation.
- Use Docker through the documented path in [DOCKER.md](./DOCKER.md), with its current build-context and runtime limitations.
- Treat any binary artifact as build-host-specific unless the spec has been made portable and revalidated.