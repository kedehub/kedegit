import os
import unittest

os.environ['KEDEGITDIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data')

from kedehub.configuration.server_config import ServerConfiguration


class KedeGitConfigurationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.server_config = ServerConfiguration().config

    def test_conf_dir_location(self):
        self.assertEqual('/Users/dimitarbakardzhiev/git/kedegit_public/tests/data', self.server_config.config_dir())

    def test_conf_get_values(self):
        self.assertEqual('localhost',self.server_config['server']['host'].get())

    def test_template_valid(self):
        self.assertEqual('localhost', self.server_config['server']['host'].get())
        self.assertEqual('test_company', self.server_config['company']['name'].get())

    def test_conf_get_repo_values(self):
        self.assertEqual('https://gitlab.com/Company_Name/repository_name.git',self.server_config['repos'][0]['origin'].get())

if __name__ == '__main__':
    unittest.main()
