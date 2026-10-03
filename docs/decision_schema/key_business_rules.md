# Key Business Rules

## Normalized Rules

| Rule ID | Statement | Source | Confidence | Notes |
|---------|-----------|--------|------------|-------|
| R1 | WHEN `KEDEGITDIR` is set THEN KEDEGit uses that directory as an override configuration directory. | Specs | High | |
| R2 | IF `config.yaml` is missing or lacks required `server` or `company` fields THEN KEDEGit terminates during startup validation. | Both | High | |
| R3 | WHEN a repository is added without an explicit repository configuration file THEN KEDEGit uses `kede-config.json` from the main configuration directory. | Source Code | High | |
| R4 | IF `sourceFiles` is not defined in the repository configuration THEN all repository files are eligible for analysis unless excluded later. | Source Code | High | |
| R5 | IF a file matches `excludedSourceFiles` THEN it is excluded from analysis even if `sourceFiles` would otherwise include it. | Source Code | High | |
| R6 | IF the same origin, repository path, and configuration file path are already stored in `config.yaml` THEN KEDEGit does not append a duplicate repository entry. | Source Code | High | |
| R7 | WHEN a repository is added to a project THEN KEDEGit ensures the project exists, saves the repository, links it to the project, and starts commit processing. | Both | High | |
| R8 | IF `--earliest-commit-date` is provided during project initialization or repository addition THEN commits earlier than that date are ignored. | Both | High | |
| R9 | IF `bulk-import-repos` is run without `-p` THEN KEDEGit initializes a separate new project for each imported repository. | Specs | High | |
| R10 | IF a clone-import command would create a project name that already exists THEN KEDEGit assigns a sequentially suffixed project name instead. | Specs | High | |
| R11 | WHEN `update-projects` runs THEN KEDEGit analyzes new commits, updates template and fraud filtering, and recalculates KEDE statistics. | Both | High | |
| R12 | IF `update-projects` is called with one or more `-p` project IDs THEN only those projects are updated. | Specs | High | |
| R13 | IF `update-projects` is called with `--clean` THEN KEDEGit deletes existing project commit data before reanalyzing all commits. | Both | High | |
| R14 | IF `update-projects` or clone-import commands are called with `--temp` THEN repositories are analyzed from temporary clones and those temporary clones are deleted afterward. | Specs | High | |
| R15 | WHEN `templates update` is run THEN template detection is applied automatically without user prompts. | Both | High | |
| R16 | WHEN `templates find` is run THEN suspected template commits are shown for user review and only commits explicitly confirmed with yes are saved as templates. | Both | High | |
| R17 | IF `templates find` is run without `-r` THEN the reporting interval defaults to quarterly `q`, and valid alternatives include weekly `w` and daily `d`. | Both | High | |
| R18 | WHEN KEDEGit analyzes repositories THEN source code and commit messages remain on local premises and are not copied to KEDEHub. | Specs | High | |
| R19 | WHEN an organization uses multiple local clients THEN data from all clients is stored under the same company name, although one shared client is recommended. | Specs | High | |
| R20 | WHEN `update-repos` runs THEN KEDEGit refreshes local repository clones without running the project statistics pipeline. | Both | High | |
| R21 | IF KEDEGit already has a last stored commit timestamp for a repository THEN only later commits are processed on subsequent runs. | Source Code | High | |
| R22 | IF a commit has more than one parent THEN KEDEGit does not calculate diff statistics for that commit. | Source Code | Medium | The code path still appears to persist the commit record with default zeroed statistics. |