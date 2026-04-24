# Dependencies

This page is for maintainers who need to understand where KEDEGit dependencies are declared today, which ones commonly fail on new machines, and which non-Python tools the repository assumes are available.

## Current dependency sources

The repository currently has two dependency declarations with different purposes.

- `requirements.txt` is the authoritative full environment snapshot for day-to-day development and runtime. It is a pinned list and is also what the current Docker image installs with `pip install -r requirements.txt`.
- `setup.py` is packaging metadata for `pip install .`, but its `install_requires` list currently contains only `gitpython`, `python-dateutil`, and `beautifultable`.

That mismatch matters in practice: `pip install .` or `pip install -e .` from the current `setup.py` metadata alone does not install the full runtime and test environment that the repository expects. For maintainer workflows, treat `requirements.txt` as the source of truth until `setup.py` is aligned.

## Native and heavy Python dependencies

Several pinned packages are common sources of install failures when a wheel is unavailable for the target Python version, platform, or architecture.

### `cffi` and `cryptography`

Both are pinned in `requirements.txt`. They are classic native-extension dependencies and are often the first packages to fail on fresh machines without a compiler toolchain or system headers.

Typical prerequisites when wheels are not available:

- macOS: Xcode Command Line Tools
- Linux: `gcc`/`build-essential`, plus the usual OpenSSL and libffi development headers for source builds
- Windows: MSVC Build Tools

### `Levenshtein` and `python-Levenshtein`

Both packages are pinned in `requirements.txt`, and the code imports `Levenshtein.editops` directly in `kedehub/gitclient/levenshtein_utility.py`. Tests under `tests/gitclient/` also import it directly.

These packages commonly install from wheels, but source builds still need a working compiler. If these fail to build, diff-stat and line-edit calculations around `levenshtein_utility.py` will not work.

### `numpy`, `pandas`, and `scipy`

The analytics side of the repository depends on the scientific stack:

- `kedehub/services/template_finder.py` imports `numpy` and `pandas`
- `kedehub/services/kede_service.py` imports `pandas`
- `kedehub/services/outliers_service.py` imports `pandas`
- tests and test data under `tests/` also exercise `pandas`, `numpy`, and `scipy`

These packages are large, platform-sensitive, and are a practical hotspot whenever Python is upgraded or contributors work on less common architectures. Prefer wheel-based installs where possible; otherwise expect compiler and system-library requirements to surface quickly.

## OS and tool dependencies

### `git` is required

KEDEGit relies on GitPython, but the repository does not work with the Python package alone. The clone, update, and repository-inspection paths call into GitPython objects that expect the `git` executable to be available on `PATH`.

This affects at least:

- clone flows in `kedehub/gitcloner/`
- update flows in `kedehub/gitupdater/gitupdater.py`
- repository inspection and diff/stat work in `kedehub/gitclient/git_utility.py` and `kedehub/kedegit.py`

If `git` is missing, maintainers should expect clone and update commands to fail, and repository analysis commands may fail as soon as they attempt to open or query a repository.

### Compiler toolchains are a practical prerequisite

Because the pinned environment includes native extensions and the scientific stack, contributor machines often need a working compiler toolchain even when the final install usually comes from wheels.

The current Docker image makes that assumption explicit by installing:

- `gcc`
- `build-essential`
- `libpq-dev`

Those packages are installed in `dockerize/Dockerfile` before `pip install -r requirements.txt`. Maintainers troubleshooting local install failures should treat the Dockerfile as the clearest statement of the current build-tool expectation.

## Docker-specific constraint

The current Docker image does not install `git`.

`dockerize/Dockerfile` installs build packages, copies the Python sources, and installs `requirements.txt`, but its `apt-get install` line does not include `git`. The result is that Python dependencies may install successfully while git-backed workflows still fail inside the container.

Impact on current flows:

- clone/import flows that need to reach remote repositories are not fully supported in the current image
- update flows that call `git pull`, inspect remotes, or query branch state are not fully supported in the current image
- any maintainer expecting the container to behave like a full development environment should add `git` first or treat the image as limited to commands that do not require repository cloning/updating

## Maintainer guidance

- Use `requirements.txt` when creating or refreshing a maintainer environment.
- Treat `setup.py` as incomplete packaging metadata until its dependency list is synchronized with the pinned environment.
- Check compiler toolchains first when installs fail on `cffi`, `cryptography`, `Levenshtein`, `numpy`, `pandas`, or `scipy`.
- Check `git --version` early when debugging clone, update, or repository-inspection failures, especially inside Docker.