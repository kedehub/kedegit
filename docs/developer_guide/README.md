# Developer Guide

This guide is for contributors working on KEDEGit from source.

- Start with [ONBOARDING.md](./ONBOARDING.md) for environment setup, config discovery, smoke checks, and a safe local test subset.
- Use [REPO_TOUR.md](./REPO_TOUR.md) for a contributor-focused map of the repository and a concrete reading order.
- Use [ARCHITECTURE.md](./ARCHITECTURE.md) for the subsystem boundaries, main pipelines, configuration split, and command-to-handler-to-service map.
- Use the subsystem pages under [subsystems/](./subsystems/) when you need implementation detail by layer:
	- [CLI_AND_ORCHESTRATION.md](./subsystems/CLI_AND_ORCHESTRATION.md)
	- [CONFIGURATION.md](./subsystems/CONFIGURATION.md)
	- [GIT_CLONING_AND_DIFF_STATS.md](./subsystems/GIT_CLONING_AND_DIFF_STATS.md)
	- [HTTP_CLIENT_AND_AUTH.md](./subsystems/HTTP_CLIENT_AND_AUTH.md)
	- [SERVICES_LAYER.md](./subsystems/SERVICES_LAYER.md)
- Use [BUILD_AND_RELEASE.md](./BUILD_AND_RELEASE.md) for the current state of run-from-source, editable install caveats, and PyInstaller packaging.
- Use [DOCKER.md](./DOCKER.md) for the current Docker build and runtime caveats.
- Use [DEPENDENCIES.md](./DEPENDENCIES.md) for the current Python dependency sources, native build hotspots, and non-Python tool assumptions.
- Use [CONTRIBUTING.md](./CONTRIBUTING.md) for a repo-accurate example workflow that adds a small offline-safe CLI feature and validates it locally.
- Use [TESTING.md](./TESTING.md) for the current split between offline-safe tests and opt-in integration or environment-coupled tests.
- Use [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) when startup fails before a command reaches its main logic.

Phase 1 covers first local setup. Phase 2 adds contributor-facing build, packaging, and Docker guidance grounded in the current repository behavior. Phase 3 adds a concise repository tour for new contributors. Phase 4 adds architecture and subsystem documentation so contributors can place changes in the right layer.
Phase 5 adds maintainer-focused dependency notes, including the current `requirements.txt` versus `setup.py` mismatch and Docker/runtime tool constraints.
Phase 6 adds a contributor workflow for making a small CLI change and validating it with the safe local test path before opting into heavier test areas.