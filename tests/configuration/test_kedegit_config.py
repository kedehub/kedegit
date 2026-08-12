import os
import unittest

os.environ['KEDEGITDIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data')

from kedehub.configuration.server_config import ServerConfiguration
from tests import working_directory, create_temporary_copy


class KedeGitConfigurationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.server_config = ServerConfiguration().config

    def test_conf_dir_location(self):
        expected_dir = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data'))
        self.assertEqual(expected_dir, os.path.normpath(self.server_config.config_dir()))

    def test_conf_get_values(self):
        self.assertEqual('localhost',self.server_config['server']['host'].get())

    def test_template_valid(self):
        self.assertEqual('localhost', self.server_config['server']['host'].get())
        self.assertEqual('test_company', self.server_config['company']['name'].get())

    def test_conf_get_repo_values(self):
        self.assertEqual('https://gitlab.com/Company_Name/repository_name.git',self.server_config['repos'][0]['origin'].get())

    def test_server_host_can_have_api_path(self):
        original_kedegitdir = os.environ.get('KEDEGITDIR')
        db_file_name = 'test_host_with_api_path.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        create_temporary_copy(db_file_path, 'config.yaml', working_directory)
        os.environ['KEDEGITDIR'] = working_directory.name

        try:
            server_config = ServerConfiguration()
            self.assertEqual('http', server_config.config['server']['protocol'].get())
            self.assertEqual('localhost/api', server_config.config['server']['host'].get())
            self.assertEqual(80, server_config.config['server']['port'].get())
            self.assertEqual('http://localhost:80/api', server_config.get_server_url())
        finally:
            if original_kedegitdir is not None:
                os.environ['KEDEGITDIR'] = original_kedegitdir
            else:
                os.environ.pop('KEDEGITDIR', None)

if __name__ == '__main__':
    unittest.main()
