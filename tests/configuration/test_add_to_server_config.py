import os
import unittest
import textwrap

from kedehub import ServerConfiguration
from tests import working_directory, create_temporary_copy

class AddRepoServerConfigTest(unittest.TestCase):

    def test_add_new_repo(self):
        db_file_name = 'unit_test_config.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        temp_file_path = create_temporary_copy(db_file_path, 'config.yaml', working_directory)
        os.environ['KEDEGITDIR'] = working_directory.name
        server_config = ServerConfiguration()

        origin = 'http://git.test.com/test_company/test_repo.git'
        repository_path = '/Users/dimitarbakardzhiev/git/test_repo'
        configuration_file_path = '/Users/dimitarbakardzhiev/git/kedehub/kede-config.json'

        yaml = server_config.add_new_repo(origin, repository_path, configuration_file_path)

        expected_config = textwrap.dedent("""
                server:
                    protocol: http
                    host: localhost
                    port: 5000
                
                company:
                    name: test_company
                    user: af9b995c-956e-49ad-a6ac-26a72613f075
                    token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWY5Yjk5NWMtOTU2ZS00OWFkLWE2YWMtMjZhNzI2MTNmMDc1IiwiY29tcGFueV9uYW1lIjoidGVzdF9jb21wYW55IiwiYXVkIjoia2VkZWh1YjpzaWduaW4iLCJleHAiOjE3MTMyMjQyMjR9.eVMZAn_yrZJg9ITmwm6iWIgkjehCbwfqZuuZlz-r3gU
                
                repos:
                -   origin: https://gitlab.com/Company_Name/repository_name.git
                    repository_path: /Users/dimitarbakardzhiev/git/kedegit/tests/data/repository
                    configuration_file_path: /Users/dimitarbakardzhiev/git/kedegit/tests/data/repo-config.json
                -   origin: http://git.elando.bg/eLando/azbg_virtual_pos.git
                    repository_path: /Users/dimitarbakardzhiev/git/kedegit/tests/data/azbg_virtual_pos
                    configuration_file_path: /Users/dimitarbakardzhiev/git/kedegit/tests/data/azbg_virtual_pos-config.json
                -   origin: https://gitlab.com/Company_Name/sub_repository_name.git
                    repository_path: /Users/dimitarbakardzhiev/git/kedegit/tests/data/subrepository
                    configuration_file_path: /Users/dimitarbakardzhiev/git/kedegit/tests/data/repo-config.json
                -   origin: http://git.test.com/test_company/test_repo.git
                    repository_path: /Users/dimitarbakardzhiev/git/test_repo
                    configuration_file_path: /Users/dimitarbakardzhiev/git/kedehub/kede-config.json
        """).strip()
        self.assertEqual(expected_config, yaml)

        with open(server_config.get_file_name(), mode="r") as cfg_file:
            self.assertEqual(expected_config,cfg_file.read())

    def test_add_first_repo(self):
        db_file_name = 'unit_test_empty_config.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        temp_file_path = create_temporary_copy(db_file_path, 'config.yaml', working_directory)
        os.environ['KEDEGITDIR'] = working_directory.name
        server_config = ServerConfiguration()

        origin = 'http://git.test.com/test_company/test_repo.git'
        repository_path = '/Users/dimitarbakardzhiev/git/test_repo'
        configuration_file_path = '/Users/dimitarbakardzhiev/git/kedehub/kede-config.json'

        yaml = server_config.add_new_repo(origin, repository_path, configuration_file_path)

        expected_config = textwrap.dedent("""
                    server:
                        protocol: http
                        host: localhost
                        port: 5000
                    
                    company:
                        name: test_company
                        user: af9b995c-956e-49ad-a6ac-26a72613f075
                        token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWY5Yjk5NWMtOTU2ZS00OWFkLWE2YWMtMjZhNzI2MTNmMDc1IiwiY29tcGFueV9uYW1lIjoidGVzdF9jb21wYW55IiwiYXVkIjoia2VkZWh1YjpzaWduaW4iLCJleHAiOjE3MTMyMjQyMjR9.eVMZAn_yrZJg9ITmwm6iWIgkjehCbwfqZuuZlz-r3gU
                    repos: [{origin: 'http://git.test.com/test_company/test_repo.git', repository_path: /Users/dimitarbakardzhiev/git/test_repo, configuration_file_path: /Users/dimitarbakardzhiev/git/kedehub/kede-config.json}]
        """).strip()
        self.assertEqual(expected_config, yaml)

        with open(server_config.get_file_name(), mode="r") as cfg_file:
            self.assertEqual(expected_config, cfg_file.read())

if __name__ == '__main__':
    unittest.main()
