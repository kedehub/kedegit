import confuse
import sys

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
        # https://confuse.readthedocs.io/en/latest/usage.html
        self.config = confuse.Configuration(APP_NAME)
        print('Confing dir: '+ self.config.config_dir())
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
            repos.append(odict)
        except(confuse.NotFoundError):
            self.config.add({'repos':[odict] })

        yaml = self.config.dump().strip()

        with open(self.config.sources[0].filename, mode="w") as cfg_file:
            cfg_file.write(yaml)

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