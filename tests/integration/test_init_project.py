import os
from collections import namedtuple

from tests.kedehub_test_load_db_once import KedeHubLoadDBOnceTest
from kedehub.__main__ import add_repository_to_a_project, bulk_add_repos_from_dir
from kedehub.services.commit_service import get_commits_per_project
from kedehub.kedegit import iter_sources


class KedeGitInitProjectTest(KedeHubLoadDBOnceTest):

    @classmethod
    def setUpClass(cls):
        super(KedeGitInitProjectTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(KedeGitInitProjectTest, cls).tearDownClass()

    def test_project_name_is_property_of_kedegit_object(self):
        self.assertEqual(self.kedegit.project_name, 'test')

    def test_add_repository_to_a_project(self):
        repository_path = os.path.join(self.current_directory, '../tests/data', 'repository')
        configuration_path = os.path.join(self.current_directory, '../tests/data', 'repo-config.json')
        Options = namedtuple('Options', ['project', 'repository','configuration','earliest_commit_date'])
        count_processed_committs, project_name = add_repository_to_a_project(Options(**{'project':'test',
                                        'repository': os.path.abspath(repository_path),
                                        'configuration':os.path.abspath(configuration_path),
                                        'earliest_commit_date': None
                                               }))

        self.assertEqual(6, count_processed_committs)
        self.assertEqual('test', project_name)

    def test_bulk_add_repos_from_dir_one_project(self):
        workdir = os.path.abspath(os.path.join(self.current_directory, '../tests/data'))
        Options = namedtuple('Options', ['workdir', 'project'])
        success_import, number_or_repo_dirs, project_names = bulk_add_repos_from_dir(Options(**{'workdir':workdir,
                                                                                 'project':'test'}))

        self.assertEqual(3, success_import)
        self.assertEqual(4, number_or_repo_dirs)
        self.assertEqual({'test'}, project_names)

    def test_bulk_add_repos_from_dir_three_projects(self):
        workdir = os.path.abspath(os.path.join(self.current_directory, '../tests/data'))
        Options = namedtuple('Options', ['workdir', 'project'])
        success_import, number_or_repo_dirs, project_names = bulk_add_repos_from_dir(Options(**{'workdir':workdir,
                                                                                 'project':None}))

        self.assertEqual(3, success_import)
        self.assertEqual(4, number_or_repo_dirs)
        self.assertSetEqual({'repository_name', 'azbg_virtual_pos', 'sub_repository_name'}, project_names)


