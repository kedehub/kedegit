V# Technical Elements Reference

## Elements

| Identifier | Type | Description | Attributes | Notes |
|------------|------|-------------|------------|-------|
| python -m kedehub | cli-command | Canonical way to run the application from source and in Docker. | Module invocation; used as the documented entrypoint. | The developer guide states there is no installed console script entrypoint. |
| --help | cli-option | Shows CLI usage information for the module entrypoint. | Used in first-run smoke checks. | Still requires valid config discovery because config loads at import time. |
| init-project | cli-command | Creates a project and imports one local repository into it. | Positionals: project, repository; options: -c, --configuration, --earliest-commit-date. | Calls the same handler as add-repository in the current code. |
| add-repository | cli-command | Imports one local repository into an existing project. | Positionals: project, repository; options: -c, --configuration, --earliest-commit-date. | Current implementation overlaps with init-project. |
| update-projects | cli-command | Imports new commits for one or more existing projects. | Options: -p, --project, --temp, --no-temp, --clean, --no-clean. | If -p, --project is omitted, the command updates all projects. |
| update-repos | cli-command | Updates all existing local repositories from their remotes. | No scoped options in the current parser. |  |
| list-projects | cli-command | Lists the names of existing projects. | No scoped options in the current parser. |  |
| list-sources | cli-command | Lists source files and test lines for a repository. | Positional: repository; option: -c, --configuration. | The guide uses it as a local diagnostics command. |
| summary | cli-command | Prints a summary of the current state of one project. | Positional: project; option: -o, --output-file. | Writes to stdout unless an output file is provided. |
| clone-import-github | cli-command | Clones and imports GitHub repositories for an organization. | Options: --workdir, --org, --token, --temp, --no-temp, -p, --project. | Bulk organization import path. |
| clone-import-github-repo | cli-command | Clones and imports one GitHub repository. | Options: --workdir, --url, --org, --token, --temp, --no-temp. | Single-repository clone and import path. |
| clone-github-repo | cli-command | Clones one GitHub repository without importing it into the backend. | Options: --workdir, --url, --org, --token, --temp, --no-temp. | Clone-only variant of the GitHub flow. |
| clone-import-gogs | cli-command | Clones and imports Gogs repositories. | Options: --workdir, --host, --username, --token, --temp, --no-temp, -p, --project. | Bulk provider import path. |
| clone-import-gogs-repo | cli-command | Clones and imports one Gogs repository. | Options: --workdir, --url, --host, --username, --token, --temp, --no-temp. | Single-repository Gogs flow. |
| clone-import-gitlab-server | cli-command | Exposes a GitLab Server bulk clone and import command in the parser. | Options: --workdir, --host, --token. | Parser-visible in the current CLI, but the handler is still a stub. |
| clone-import-bitbucket-cloud | cli-command | Exposes a Bitbucket Cloud bulk clone and import command in the parser. | Options: --workdir, --workspaceid, --username, --pwd. | Parser-visible in the current CLI, but the handler is still a stub. |
| bulk-import-repos | cli-command | Bulk imports already cloned repositories from a directory. | Options: --workdir, -p, --project. | Uses each directory entry under the given workdir. |
| fix-kede | cli-command | Repairs wrongly calculated KEDE data for one or more projects. | Option: -p, --project. | If -p, --project is omitted, the command operates on all projects. |
| stats calculate-kede | cli-command | Calculates KEDE statistics for the selected projects and authors. | Options: -p, --project; -a, --author. | Implemented as the stats command with type choice calculate-kede. |
| stats calculate-weekly-kede | cli-command | Calculates weekly KEDE statistics for the selected projects and authors. | Options: -p, --project; -a, --author. | Implemented as the stats command with type choice calculate-weekly-kede. |
| ranklist calculate | cli-command | Calculates a rank list over a selected date window. | Options: -lw, --last_week; -td, --today. | Implemented as the ranklist command with type choice calculate. |
| templates find | cli-command | Finds committed templates in interactive mode. | Options: -o, --output-file; -p, --project; -a, --author; -r, --reporting_interval. | Implemented as the templates command with type choice find. |
| templates update | cli-command | Updates templates without prompting the user. | Options: -o, --output-file; -p, --project; -a, --author; -r, --reporting_interval. | Implemented as the templates command with type choice update. |
| -c, --configuration | cli-option | Supplies the path to a repository configuration file. | Used by init-project, add-repository, and list-sources. | Points to the JSON repo configuration file contract. |
| --earliest-commit-date | cli-option | Ignores commits before a given date. | Used by init-project and add-repository. | The current implementation parses the value as a date. |
| -o, --output-file | cli-option | Writes command output to a file instead of only showing it on screen. | Used by summary and templates. | The templates help text still advertises a graph-oriented output file. |
| -p, --project | cli-option | Selects one or more project names for a command. | Used by update-projects, clone-import-github, clone-import-gogs, bulk-import-repos, fix-kede, stats, and templates. | The current CLI reuses the same option with both single-value and multi-value semantics. |
| -a, --author | cli-option | Filters stats and template operations by author name. | Used by stats and templates; accepts zero or more values. |  |
| --workdir | cli-option | Sets the directory used for clone or bulk import operations. | Used by clone and bulk-import commands. |  |
| --org | cli-option | Supplies the GitHub organization name for GitHub clone flows. | Used by clone-import-github, clone-import-github-repo, and clone-github-repo. |  |
| --url | cli-option | Supplies the clone URL for a single repository flow. | Used by clone-import-github-repo, clone-github-repo, and clone-import-gogs-repo. |  |
| --token | cli-option | Supplies an access token for provider-backed clone flows. | Used by GitHub, Gogs, and GitLab Server clone-import commands. |  |
| --host | cli-option | Supplies the provider host for Gogs or GitLab Server flows. | Used by clone-import-gogs, clone-import-gogs-repo, and clone-import-gitlab-server. |  |
| --username | cli-option | Supplies the provider username for Gogs or Bitbucket Cloud flows. | Used by clone-import-gogs, clone-import-gogs-repo, and clone-import-bitbucket-cloud. |  |
| --workspaceid | cli-option | Supplies the Bitbucket Cloud workspace identifier. | Used by clone-import-bitbucket-cloud. | The exact long option in the current parser uses workspaceid without a hyphen. |
| --pwd | cli-option | Supplies the Bitbucket Cloud password value. | Used by clone-import-bitbucket-cloud. | The current CLI exposes pwd rather than password. |
| --temp | cli-option | Enables temporary clone behavior for commands that support it. | Boolean flag paired with --no-temp. | Common across several provider import flows and update-projects. |
| --no-temp | cli-option | Disables temporary clone behavior for commands that support it. | Boolean flag paired with --temp. | Common across several provider import flows and update-projects. |
| --clean | cli-option | Enables cleanup before importing new commits. | Boolean flag paired with --no-clean. | Used by update-projects. |
| --no-clean | cli-option | Disables cleanup before importing new commits. | Boolean flag paired with --clean. | Used by update-projects. |
| -lw, --last_week | cli-option | Supplies the starting Monday date for ranklist calculation. | Used by ranklist calculate. |  |
| -td, --today | cli-option | Supplies the end date boundary for ranklist calculation. | Used by ranklist calculate. |  |
| -r, --reporting_interval | cli-option | Selects the reporting interval for template analysis. | Used by templates; choices: y, q, m, w, d; default: q. | The current long option uses an underscore in its exact name. |
| KEDEGITDIR | other | Environment variable that overrides the config directory used for config discovery. | Set before importing or running the CLI. | The developer guide recommends it for reliable local setup. |
| config.yaml | file-format | Global YAML configuration file for server connection, credentials, and local repository registry. | YAML; default lookup is under the KedeGit config directory or the directory pointed to by KEDEGITDIR. | The current loader validates ASCII-only content and rejects a UTF-8 BOM. |
| server.protocol | config-key | Configures the server URL protocol. | Required YAML key under config.yaml. |  |
| server.host | config-key | Configures the server host name. | Required YAML key under config.yaml. |  |
| server.port | config-key | Configures the server port number. | Required YAML key under config.yaml. |  |
| company.name | config-key | Configures the company name used by backend requests. | Required YAML key under config.yaml. | Used in the token endpoint path described by the developer guide. |
| company.user | config-key | Configures the backend user name. | Required YAML key under config.yaml. |  |
| company.token | config-key | Configures the backend user token or password-flow seed value. | Required YAML key under config.yaml. |  |
| repos | config-key | Declares the local repository registry stored in the global YAML config. | YAML sequence; entry fields: origin, repository_path, configuration_file_path. | The guide documents exact origin-string matching when enriching repository data. |
| origin | field-name | Stores the remote origin string for one repo registry entry. | Field inside each repos item. | Matching is exact, so SSH and HTTPS variants are treated as different values. |
| repository_path | field-name | Stores the local path for one repo registry entry. | Field inside each repos item. |  |
| configuration_file_path | field-name | Stores the path to the per-repository JSON configuration file. | Field inside each repos item. |  |
| kede-config.json | file-format | Per-repository JSON configuration file used for source and test matching rules. | JSON; optional; missing file is treated as an empty config. | The current code and guide use this exact filename as the default contract name. |
| sourceFiles | config-key | Declares glob patterns for included source files. | JSON key in kede-config.json; accepts a string or list of strings. | Matching supports recursive glob syntax such as **. |
| excludedSourceFiles | config-key | Declares glob patterns for excluded source files. | JSON key in kede-config.json; accepts a string or list of strings. | Applied as an exclusion filter after sourceFiles. |
| testFiles | config-key | Declares glob patterns for test files. | JSON key in kede-config.json; accepts a string or list of strings. | Documented as part of the repo config surface. |
| testLineRegex | config-key | Declares a regular expression used to identify test lines. | JSON key in kede-config.json; value is a regex string. | Compiled by the current config loader when present. |
| /root/.config/KedeGit | other | Container-side config directory expected by the Docker workflow. | Mount target for a directory that contains config.yaml. | Documented in the developer guide Docker flow. |
| /companies/&lt;company_name&gt;/token | api | Token endpoint path pattern derived from the configured server URL and company name. | Path pattern documented in the auth subsystem guide. | The scoped sources describe the path shape but not the HTTP method. |