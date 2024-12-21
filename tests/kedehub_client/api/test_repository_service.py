import unittest
import datetime
import os
from tests.kedehub_test_load_db_once import KedeHubLoadDBOnceTest
from kedehub.services.dro.repository_dto import Repository
from kedehub.services.repository_service import load_company_repositories, load_reposotories_for_project
from kedehub.services.project_service import assign_new_repo_to_existing_project
from kedehub_client import get_sync_apis

class KedeHubRepositoryServiceTest(KedeHubLoadDBOnceTest):

    @classmethod
    def setUpClass(cls):
        super(KedeHubRepositoryServiceTest, cls).setUpClass()
        cls.start_date = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        cls.kedegit.add_repository(os.path.join(cls.current_directory, '../tests/data', 'azbg_virtual_pos'),
                                    os.path.join(cls.current_directory, '../tests/data', 'azbg_virtual_pos-config.json'),
                                    earliest_date=cls.start_date)


    @classmethod
    def tearDownClass(cls):
        super(KedeHubRepositoryServiceTest, cls).tearDownClass()

    def test_load_all_repositories(self):

        expected_repositories = [
                                    Repository(id=1,
                                               origin="http://git.elando.bg/eLando/azbg_virtual_pos.git",
                                            repository_path=os.path.abspath(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos')),
                                            configuration_file_path=os.path.abspath(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json')),
                                            head_commit_id=None,
                                            start_time=datetime.datetime(2018, 1, 1, 0, 0),
                                            start_time_utc_offset=0)
        ]
        repositories = load_company_repositories()
        self.assertTrue(len(repositories)>0)
        self.assertEqual(expected_repositories[0].configuration_file_path, repositories[0].configuration_file_path)
        self.assertEqual(expected_repositories[0].repository_path, repositories[0].repository_path)
        self.assertEqual(expected_repositories[0].start_time, repositories[0].start_time)

    def test_load_reposotories_for_project(self):

        expected_repositories = [
                                    Repository(id=1,
                                            origin = "http://git.elando.bg/eLando/azbg_virtual_pos.git",
                                            repository_path=os.path.abspath(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos')),
                                            configuration_file_path=os.path.abspath(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json')),
                                            head_commit_id=None,
                                            start_time=datetime.datetime(2018, 1, 1, 0, 0),
                                            start_time_utc_offset=0)
        ]
        self.maxDiff=None
        repositories = load_reposotories_for_project('test')
        self.assertTrue(len(repositories)==1)
        self.assertEqual(expected_repositories[0].configuration_file_path, repositories[0].configuration_file_path)
        self.assertEqual(expected_repositories[0].repository_path, repositories[0].repository_path)
        self.assertEqual(expected_repositories[0].start_time, repositories[0].start_time)

    def test_load_non_existant_reposotories_for_project(self):

        expected_repositories = [
                                    Repository(id=1,
                                            origin = "http://git.elando.bg/eLando/azbg_virtual_pos.git",
                                            repository_path=os.path.abspath(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos')),
                                            configuration_file_path=os.path.abspath(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json')),
                                            head_commit_id=None,
                                            start_time=datetime.datetime(2018, 1, 1, 0, 0),
                                            start_time_utc_offset=0)
        ]
        self.maxDiff=None
        repo = Repository(origin = "http://git.elando.bg/eLando/azbg_virtual_pos_NONE.git",repository_path = os.path.join(self.current_directory, '../tests/data', 'repository'),
                          configuration_file_path = 'repo-config.json')
        # new_repo = save_new_repo(repo.origin, repo.configuration_file_path, repo.start_time, repo.repository_path)
        new_repo = get_sync_apis().repository_api.save_new_repository(repo)
        assign_new_repo_to_existing_project('test', new_repo.id)

        repositories = load_reposotories_for_project('test')
        self.assertTrue(len(repositories)==1)
        self.assertEqual(expected_repositories[0].configuration_file_path, repositories[0].configuration_file_path)
        self.assertEqual(expected_repositories[0].repository_path, repositories[0].repository_path)
        self.assertEqual(expected_repositories[0].start_time, repositories[0].start_time)

    def test_load_repository_with_no_local_folder(self):
        expected_repositories = [
            Repository(id=1,
                       origin="http://git.elando.bg/eLando/azbg_virtual_pos.git",
                       repository_path=os.path.abspath(
                           os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos')),
                       configuration_file_path=os.path.abspath(
                           os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json')),
                       head_commit_id=None,
                       start_time=datetime.datetime(2018, 1, 1, 0, 0),
                       start_time_utc_offset=0)
        ]
        self.maxDiff = None
        repo = Repository(origin="http://git.elando.bg/eLando/azbg_virtual_pos_NONE.git",
                          repository_path=os.path.join(self.current_directory, '../tests/data', 'repository'),
                          configuration_file_path='repo-config.json')
        # new_repo = save_new_repo(repo.origin, repo.configuration_file_path, repo.start_time, repo.repository_path)
        new_repo = get_sync_apis().repository_api.save_new_repository(repo)
        assign_new_repo_to_existing_project('test', new_repo.id)

        repositories = load_reposotories_for_project('test')
        self.assertTrue(len(repositories) == 1)
        self.assertEqual(expected_repositories[0].configuration_file_path, repositories[0].configuration_file_path)
        self.assertEqual(expected_repositories[0].repository_path, repositories[0].repository_path)
        self.assertEqual(expected_repositories[0].start_time, repositories[0].start_time)

if __name__ == '__main__':
    unittest.main()
