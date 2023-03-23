import os
from tests.kedehub_test_load_db_once import KedeHubLoadDBOnceTest
from kedehub.services.commit_service import get_commits_per_project
from kedehub.kedegit import iter_sources


class KedeGitRepositoryTest(KedeHubLoadDBOnceTest):

    @classmethod
    def setUpClass(cls):
        super(KedeGitRepositoryTest, cls).setUpClass()
        cls.kedegit.add_repository(os.path.join(cls.current_directory, '../tests/data', 'repository'),
                                    os.path.join(cls.current_directory, '../tests/data', 'repo-config.json'))

    @classmethod
    def tearDownClass(cls):
        super(KedeGitRepositoryTest, cls).tearDownClass()

    def test_project_name_is_property_of_kedegit_object(self):
        self.assertEqual(self.kedegit.project_name, 'test')

    def test_repository_is_processed_into_database_after_adding(self):
        # To get the commit count across all branches:
        # git rev-list --all --count
        commits = get_commits_per_project(self.kedegit.project_name,
                                          self.kedegit._shas_to_commits)
        self.assertEqual(6, len(commits))

    def test_commit_timestamps_have_correct_time(self):
        initial_commit = self._fetch_commit(KedeGitRepositoryTest._main_repo_initial_commit_hexsha )
        self.assertEqual(initial_commit.commit_time_tz().hour, 11)

    def test_initial_commit_line_counts_are_correct(self):
        initial_commit = self._fetch_commit(KedeGitRepositoryTest._main_repo_initial_commit_hexsha)
        self.assertEqual(initial_commit.added_lines, 14)
        self.assertEqual({'Text': 17},initial_commit.lang_count)

    def test_second_commit_line_counts_are_correct(self):
        initial_commit = self._fetch_commit(KedeGitRepositoryTest._main_repo_initial_commit_hexsha)
        second_commit = self._fetch_commit(KedeGitRepositoryTest._main_repo_second_commit_hexsha)
        self.assertEqual(initial_commit.added_lines, 14)
        self.assertEqual(second_commit.added_lines, 4)
        self.assertEqual({'Text': 17},initial_commit.lang_count)
        self.assertEqual({'Text': 4},second_commit.lang_count)

    def test_sources_are_iterated_based_on_configuration(self):
        repository_path = os.path.join(self.current_directory, '../tests/data', 'repository')
        configuration_path = os.path.join(self.current_directory, '../tests/data', 'repo-config.json')
        files = list(iter_sources(repository_path, configuration_path))
        file_names = [name for (file_type, name) in files]
        self.assertIn(('source-file', 'file1.txt'), files)
        self.assertNotIn('file.dat', file_names)

