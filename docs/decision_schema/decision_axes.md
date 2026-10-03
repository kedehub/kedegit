# Decision Axes (Test Input Space)

## Axes

### A1 — Operation context
- **Values:** help or usage invocation; project initialization; repository addition; bulk repository import; project update; local repository update; repository cloning only; repository clone-and-import; project listing; source listing; summary generation; template workflow; KEDE calculation workflow; ranklist workflow; KEDE repair
- **Notes:** `--help` is included because the authoritative CLI contract documents it as a distinct invocation path that still depends on valid config discovery. Concrete CLI commands and subcommands are intentionally normalized into behavior-level workflow families so that A11 and A15 remain independent subcommand-choice axes rather than duplicates.

### A2 — Command availability state
- **Values:** implemented; parser-visible stub
- **Notes:** `clone-import-gitlab-server` and `clone-import-bitbucket-cloud` are parser-visible in the current CLI but still stubbed in the handler layer.

### A3 — Git Repository input shape
- **Values:** one existing local Git Repository; directory of local Git Repositories; one remote Git Repository; multiple remote Git Repositories

### A4 — Code-Sharing Platform
- **Values:** GitHub; Gogs; GitLab Server; Bitbucket Cloud
- **Notes:** The repository glossary uses Code-Sharing Platform as the canonical business term; the concrete platform values come from the CLI surface and user documentation.

### A5 — Repository locator source
- **Values:** positional local repository path; directory scan via `--workdir`; remote organization or workspace listing; remote single-repository URL via `--url`; registry enrichment from `config.yaml`

### A6 — Provider access input state
- **Values:** provider inputs not applicable; locator complete and credentials complete; locator missing or invalid with credentials complete; locator complete with credentials missing or invalid; locator missing or invalid with credentials missing or invalid
- **Notes:** Depending on the command and Code-Sharing Platform, locator inputs come from `--org`, `--host`, `--workspaceid`, or `--url`, while credential inputs come from `--token`, `--username`, or `--pwd`.

### A7 — Project selection scope
- **Values:** one selected Project; multiple selected Projects; all Projects
- **Notes:** New-Project creation and one-Project-per-import behavior are derived from the operation context rather than separate selection-scope values.

### A8 — Author targeting scope
- **Values:** all Developers; one Developer; multiple Developers
- **Notes:** The CLI flag is `-a, --author`; the canonical business object is Developer.

### A9 — Temporary clone retention policy
- **Values:** persistent local clone; temporary clone deleted after processing
- **Notes:** `--temp` selects temporary-clone behavior; omission and `--no-temp` collapse to persistent local-clone behavior.

### A10 — Project refresh mode
- **Values:** incremental update; clean reanalysis
- **Notes:** Omission and `--no-clean` collapse to the incremental update path; explicit `--clean` forces clean reanalysis.

### A11 — Template handling mode
- **Values:** automatic update; interactive find

### A12 — Interaction environment
- **Values:** interactive TTY available; non-interactive input

### A13 — Interactive confirmation state
- **Values:** confirmed; not confirmed
- **Notes:** This axis applies to interactive flows such as `templates find` and the fast-forward prompt in `update-repos`.

### A14 — Templates reporting interval
- **Values:** `y`; `q`; `m`; `w`; `d`; invalid value rejected by parser
- **Notes:** The effective default is quarterly `q` when the option is omitted.

### A15 — KEDE calculation interval
- **Values:** Daily KEDE; Weekly KEDE

### A16 — Earliest commit date input state
- **Values:** omitted; valid date; invalid date

### A17 — Ranklist window input state
- **Values:** both boundaries provided and valid; one boundary missing; invalid boundary format
- **Notes:** The authoritative CLI surface exposes `-lw, --last_week` and `-td, --today`; narrower evidence is strongest for presence and formatting, not for a separate ordering-validation branch.

### A18 — Runtime packaging context
- **Values:** run from source; Docker container; executable
- **Notes:** The CLI surface is intentionally similar across these contexts, but config discovery paths and documented host settings differ.

### A19 — Configuration directory location
- **Values:** `KEDEGITDIR` override; default config directory; Docker mount directory

### A20 — Repository configuration path source
- **Values:** explicit `-c, --configuration` path; repository-local `kede-config.json` default; configuration-directory `kede-config.json` default
- **Notes:** `list-sources` defaults to a repository-local `kede-config.json`; ingestion flows default to `kede-config.json` in the active configuration directory when `-c, --configuration` is omitted.

### A21 — Server configuration validity state
- **Values:** valid `config.yaml`; missing `config.yaml`; YAML formatting error; missing required key; UTF-8 BOM present; non-ASCII bytes present

### A22 — Repository configuration load state
- **Values:** missing file treated as empty configuration; valid empty configuration; valid populated configuration; invalid JSON; invalid `testLineRegex`; invalid pattern declaration
- **Notes:** The technical elements contract defines `sourceFiles`, `excludedSourceFiles`, and `testFiles` as a string or list of strings; declarations outside that contract are treated here as invalid pattern declarations.

### A23 — Repository registry state
- **Values:** `repos` key absent; `repos` present and malformed; `repos` present with exact `origin` match; `repos` present with no local registry match
- **Notes:** Matching is exact-string equality, so SSH and HTTPS variants remain distinct unless the stored `origin` string also matches exactly.

### A24 — KEDEHub authorization state
- **Values:** authorized session already available; session recoverable by refresh; session recoverable by login; unusable authorization credentials
- **Notes:** This is the input-side auth axis; retry and exit behavior are derived outcomes from this state plus the HTTP response path. Refresh and login terminology comes from the documented auth subsystem.

### A25 — Output sink
- **Values:** standard output; output file
- **Notes:** `summary` is the clearest documented file-output path; most other commands report directly to standard output.

### A26 — Remote interaction boundary
- **Values:** no KEDEHub API call; KEDEHub API call required

### A27 — Persistence boundary
- **Values:** local filesystem only; KEDEHub backend only; local filesystem and KEDEHub backend
- **Notes:** Local filesystem includes Git Repository clones plus local `config.yaml` and `kede-config.json` artifacts.

### A28 — View or screen scope
- **Values:** KEDEGit local client; SaaS Platform; Organizational Dashboard
- **Notes:** This axis is included because the authoritative web docs explicitly partition visible behavior across the local client, the SaaS Platform, and the Organizational Dashboard, which bounds where a workflow is allowed, shown, or persisted.

## Accounted Non-Axes

- **Required YAML keys:** `server.protocol`, `server.host`, `server.port`, `company.name`, `company.user`, and `company.token` are rule-only constraints inside A21, not independent axes, because the behavior fork is driven by validity versus missing-key failure rather than by swapping one required key for another.
- **Exact-`origin` equality:** exact matching between backend repositories and local `repos` entries remains a rule-only constraint inside A23, not a separate axis, because the externally visible branch is already modeled as matched versus unmatched registry state.
- **Token error codes:** `invalid_request`, `invalid_client`, `invalid_grant`, `unauthorized_client`, `unsupported_grant_type`, and `invalid_scope` are derived protocol details beneath A24 and do not independently change the public command families beyond success versus failure handling.
- **Analyzed change classification:** ordinary Commit, Template, and Fraudulent Code are derived classification outcomes in this repository rather than authoritative input dimensions, so they are intentionally kept out of the test input axis list.
- **Invalid work directories and filesystem permission failures:** these are kept as validation or execution rules rather than axes because the authoritative inputs do not define a stable finite business taxonomy for them beyond command failure.
- **Language detection outputs and other internal technical enumerations:** these are non-axis contextual concepts for this glossary because the supplied authoritative inputs center the decision space on CLI workflows, configuration, persistence, and reporting behavior rather than on internal classifier implementation details.