import unittest
import datetime
import os

from tests.kedegit_test import KedeGitTest
from kedehub.services.dro.repository_dto import Repository
from kedehub.services.repository_service import save_new_repo

class KedeHubSaveRepositoryServiceTest(KedeGitTest):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_save_new_repo(self):
        repo = Repository(origin = "http://git.elando.bg/eLando/azbg_virtual_pos.git",repository_path = os.path.join(self.current_directory, '../tests/data', 'repository'),
                          configuration_file_path = 'repo-config.json')

        new_repo = save_new_repo(repo.origin, repo.configuration_file_path, repo.start_time, repo.repository_path)

        self.assertTrue(new_repo.id>0)
        self.assertEqual(repo.configuration_file_path, new_repo.configuration_file_path)
        self.assertEqual(repo.repository_path, new_repo.repository_path)
        self.assertEqual(datetime.datetime(1980, 1, 1, 0, 0), new_repo.start_time)

    def test_save_duplicate_repo(self):
        repo = Repository(origin = "http://git.elando.bg/eLando/azbg_virtual_pos.git",repository_path = os.path.join(self.current_directory, '../tests/data', 'repository'),
                          configuration_file_path = 'repo-config.json')

        new_repo = save_new_repo(repo.origin, repo.configuration_file_path, repo.start_time, repo.repository_path)

        new_repo = save_new_repo(repo.origin, repo.configuration_file_path, repo.start_time, repo.repository_path)

        self.assertTrue(new_repo.id>0)
        self.assertEqual(repo.configuration_file_path, new_repo.configuration_file_path)
        self.assertEqual(repo.repository_path, new_repo.repository_path)
        self.assertEqual(datetime.datetime(1980, 1, 1, 0, 0), new_repo.start_time)


if __name__ == '__main__':
    unittest.main()
