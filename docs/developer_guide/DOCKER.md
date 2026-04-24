# Docker

This page documents the current Docker workflow in the repository as it exists today.

Docker is available as a contributor and maintainer aid, but it is not the primary supported development workflow. The supported contributor path remains run-from-source with `requirements.txt` and `python -m kedehub` from a repository checkout.

## Prerequisite: Docker service must be running

Before using the commands on this page, make sure a local Docker daemon is running.

- On Docker Desktop, start Docker Desktop and wait for it to report that Docker is running.
- On a Linux host, start the local Docker service before running `docker build` or `docker run`.

If the daemon is not running, the commands below will fail even if the `docker` CLI is installed.

## Current Docker assets

The repository currently documents Docker in two places:

- `dockerize/Dockerfile`
- `dockerize/kedegit-docker-how-to.md`

Those files are useful, but they encode assumptions about where the build is started from and what is present in the build context.

## Build context assumptions

The Dockerfile uses these copy statements:

```dockerfile
COPY kedegit/requirements.txt .
COPY kedegit/kedehub/ ./kedehub/
COPY kedegit/kedehub_client/ ./kedehub_client/
```

That means the build context is expected to contain a top-level `kedegit/` directory.

The companion how-to uses this command:

```bash
docker build --no-cache -t kedegit-image:latest -f kedegit/dockerize/Dockerfile .
```

That command only works when `.` is the parent directory that contains the repository as `./kedegit/`.

If you run the build from the repository root instead, the current Dockerfile will likely fail because paths such as `kedegit/requirements.txt` do not exist relative to that context.

In other words:

- Build from the parent directory if you want to use the Dockerfile exactly as written.
- Do not assume the current Dockerfile is repo-root portable.

## Runtime configuration path

The image creates and expects the standard config directory at:

```text
/root/.config/KedeGit
```

The current how-to mounts configuration there:

```bash
docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  --name kedegit-container \
  -v ~/git/kedegit/docs:/root/.config/KedeGit \
  kedegit-image:latest list-projects
```

That matches the config discovery model already used elsewhere in the repository. The mounted directory still needs to contain a valid `config.yaml`.

## What the image actually runs

The Dockerfile ends with:

```dockerfile
ENTRYPOINT ["python", "-u", "-m", "kedehub"]
CMD ["--help"]
```

That is aligned with the supported source-based workflow. The container also uses module execution rather than a packaged console script.

## Known issues and limitations

### Likely COPY-path mismatch from the repo root

The most immediate problem is the build-context mismatch described above. Contributors often build from the repository root, but the current Dockerfile expects the repository to appear as `kedegit/` inside a larger context.

Until the Dockerfile is adjusted, be explicit about the build location when documenting or using it.

### Git is not explicitly installed

The Dockerfile installs:

- `gcc`
- `libpq-dev`
- `build-essential`

It does not explicitly install `git`.

That matters because KEDEGit includes clone and update workflows that depend on local Git operations. If those paths are exercised inside the container, clone and update features may fail unless the base image already happens to provide `git`.

Do not assume repository-cloning or repository-updating commands work in the current image without verifying that first.

### The image is not a full portability guarantee

The current image installs dependencies from `requirements.txt` and runs `python -m kedehub`, which is a good baseline. But portability is still limited by:

- the build-context assumptions in the Dockerfile
- the need for a valid mounted config directory
- the missing explicit `git` installation for Git-backed workflows
- the fact that the Docker docs currently demonstrate one local directory layout, not a generalized contributor flow

## Practical contributor guidance

If you need Docker for local validation, treat the current workflow as a documented starting point rather than a fully hardened path.

Recommended approach:

1. Prefer run-from-source for day-to-day development and debugging.
2. If you build the image, do it from the parent directory that contains the repository as `kedegit/` so the current `COPY` statements resolve.
3. Mount a directory containing `config.yaml` to `/root/.config/KedeGit`.
4. Verify the specific command you need, especially if it clones or updates repositories.

## Maintainer follow-up for a more portable image

To make the Docker path more contributor-friendly, the next maintenance steps would be:

1. Make the Dockerfile work from the repository root as a build context.
2. Install `git` explicitly if clone and update workflows are expected to run in-container.
3. Re-test the documented `docker run` commands against the current image.
4. Update this page once the build command and supported scope are stable.

Until then, keep the Docker documentation honest: it documents the current local assumptions, not a fully portable container distribution story.