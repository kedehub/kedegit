import datetime
import os
import unittest

from tests.kedegit_test import KedeGitTest
from kedehub.services.dro.repository_dto import Repository
from kedehub import server_config
from kedehub.services import merge_repo_from_db_and_config


class KedeGitLoadReposTest(KedeGitTest):

    def setUp(self):
        super().setUp()
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'repository'))

    def tearDown(self):
        super().tearDown()

    def test_merge_one_repo(self):

        expected_repo = Repository(id=1,
                                            origin = "https://gitlab.com/Company_Name/repository_name.git",
                                            repository_path=os.path.abspath(os.path.join(self.current_directory, '../tests/data', 'repository')),
                                            configuration_file_path=os.path.abspath(os.path.join(self.working_directory.name, 'kede-config.json')),
                                            head_commit_id=None,
                                            start_time=datetime.datetime(2018, 1, 1, 0, 0),
                                            start_time_utc_offset=0)

        repo_from_db = Repository(id=1,
                                            origin = "https://gitlab.com/Company_Name/repository_name.git",
                                            head_commit_id=None,
                                            start_time=datetime.datetime(2018, 1, 1, 0, 0),
                                            start_time_utc_offset=0)
        repo_data_from_config = server_config.get_repos()

        merge_repo_from_db_and_config(repo_data_from_config, repo_from_db)

        self.assertEqual(expected_repo,repo_from_db)

    def test_merge_non_existant_repo(self):

        expected_repo = Repository(id=1,
                                            origin = "https://gitlab.com/Company_Name/repository_name_NONE.git",
                                            repository_path=None,
                                            configuration_file_path=None,
                                            head_commit_id=None,
                                            start_time=datetime.datetime(2018, 1, 1, 0, 0),
                                            start_time_utc_offset=0)

        repo_from_db = Repository(id=1,
                                            origin = "https://gitlab.com/Company_Name/repository_name_NONE.git",
                                            head_commit_id=None,
                                            start_time=datetime.datetime(2018, 1, 1, 0, 0),
                                            start_time_utc_offset=0)
        repo_data_from_config = server_config.get_repos()

        merge_repo_from_db_and_config(repo_data_from_config, repo_from_db)

        self.assertEqual(expected_repo,repo_from_db)

    def test_is_repo_present_existing_origin(self):

        repo_origin = "https://gitlab.com/Company_Name/repository_name.git"
        self.assertTrue(server_config.is_repo_present(repo_origin))

    def test_is_repo_present_non_existing_origin(self):

        repo_origin = "https://gitlab.com/Company_Name/repository_name_NONE.git"
        self.assertFalse(server_config.is_repo_present(repo_origin))

if __name__ == '__main__':
    unittest.main()
