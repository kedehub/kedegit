import confuse
import sys
import yaml

APP_NAME = 'KedeGit'


class ServerConfiguration:

    def __init__(self):

        self.template = {

            'server': {
                'protocol': str,
                'host': str,
                'port': int,
            },

            'company': {
                'name': str,
                'user': str,
                'token': str
            },
            'repos': confuse.Sequence(
                {
                    'origin': str,
                    'repository_path': str,
                    'configuration_file_path': str
                }
            )
        }

        try:
            self.config = confuse.Configuration(APP_NAME)
            print('This is your Config dir: ' + self.config.config_dir())
        except Exception as e:
            print(f"Error initializing configuration: {e}")
            sys.exit("Error initializing configuration: {e}")

        # Validate YAML file before loading
        self.validate_yaml_file(self.get_file_name())

        # Load the configuration using confuse
        self.config.get(self.template)

    def get_config_dir(self):
        return self.config.config_dir()

    def get_file_name(self):
        return self.config.sources[0].filename

    def get_company_name(self):
        return self.config['company']['name'].get()

    def get_company_user(self):
        return self.config['company']['user'].get()

    def get_user_token(self):
        return self.config['company']['token'].get()

    def add_new_repo(self, origin, repository_path, configuration_file_path):

        self.config.sources[0].default = True

        odict = confuse.OrderedDict()
        odict['origin'] = origin
        odict['repository_path'] = repository_path
        odict['configuration_file_path'] = configuration_file_path

        try:
            repos = self.config['repos'].get()
            # Check for duplicates
            existion_repo = False
            for repo in repos:
                if repo['origin'] == origin and repo['repository_path'] == repository_path and repo[
                    'configuration_file_path'] == configuration_file_path:
                    print('Duplicate repository. Not added to configuration.')
                    existion_repo = True
            if not existion_repo:
                repos.append(odict)
        except(confuse.NotFoundError):
            self.config.add({'repos':[odict] })

        yaml = self.config.dump().strip()

        try:
            with open(self.config.sources[0].filename, mode="w") as cfg_file:
                cfg_file.write(yaml)
        except IOError:
            print('IOError: An error occurred while trying to write to the configuration file.')
            raise IOError

        return yaml

    def get_repos(self):
        try:
            return self.config['repos'].get()
        except Exception as e:
            print('FATAL: Could not find repos in config file: ({}). Terminating.'.format(e))
            sys.exit(1)

    def get_server_url(self):
        return self.config['server']['protocol'].get() +'://' + self.config['server']['host'].get() + ':' + str(self.config['server']['port'].get())

    def set_file(self, file_name: str):
        self.config.set_file(file_name)

    def is_repo_present(self, repo_origin: str):
        for repo_data_from_config in self.get_repos():
            if (repo_origin == repo_data_from_config['origin']):
                return True

    def validate_yaml_file(self, file_path):
        required_keys = [
            'server.protocol',
            'server.host',
            'server.port',
            'company.name',
            'company.user',
            'company.token'
        ]

        try:
            # Check for BOM and non-ASCII characters
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                if raw_data.startswith(b'\xef\xbb\xbf'):
                    raise ValueError(
                        f"YAML file '{file_path}' contains a BOM (Byte Order Mark), which should be removed.")

                # Ensure no non-ASCII characters (optional)
                if not raw_data.isascii():
                    raise ValueError(f"YAML file '{file_path}' contains non-ASCII characters.")

            # Check for consistent line endings (LF or CRLF)
            with open(file_path, 'r', newline='') as file:
                content = file.read()
                # Check for CRLF line endings and raise an exception if found
                if '\r\n' in content:
                    raise ValueError(
                        f"YAML file '{file_path}' uses Windows-style CRLF line endings. Please use consistent LF line endings.")

            # Check for YAML syntax and missing keys
            with open(file_path, 'r') as file:
                config_data = yaml.safe_load(file)

                # Check for missing required keys
                for key in required_keys:
                    parts = key.split('.')
                    temp_data = config_data
                    for part in parts:
                        if part not in temp_data:
                            raise KeyError(f"Missing required key: '{key}'")
                        temp_data = temp_data[part]

        except yaml.YAMLError as exc:
            print(f"YAML formatting error in '{file_path}': {exc}")
            sys.exit(1)
        except FileNotFoundError:
            sys.exit(f"YAML file '{file_path}' not found!")
        except KeyError as exc:
            sys.exit(f"YAML validation error: {exc}")
