import os
from tests.kedegit_test import KedeGitTest
from kedehub.services.author_service import load_authors_per_project
from kedehub.services.project_service import load_all_project_names


class KedeGitMultipleProjectsTest(KedeGitTest):

    def _create_second_project(self):
        self.otherKedeGit = self._make_kedegit('otherTest')
        self.otherKedeGit.add_repository(os.path.join(self.current_directory, '../tests/data', 'subrepository'))

    def setUp(self):
        super().setUp()
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'repository'))

    def tearDown(self):
        super().tearDown()

    def test_second_project_is_created(self):
        self._create_second_project()
        self.assertEqual(self.otherKedeGit.project_name, 'othertest')

    def test_projects_are_inserted_in_database(self):
        self._create_second_project()
        project_names = load_all_project_names()
        self.assertEqual(sorted(project_names), ['othertest', 'test'])

    def test_commits_from_other_projects_are_not_included(self):
        self._create_second_project()
        with self.assertRaises(StopIteration):
            self._fetch_commit(KedeGitMultipleProjectsTest._main_repo_initial_commit_hexsha, kedegit=self.otherKedeGit)

    def test_authors_from_other_projects_are_not_included(self):
        self._create_second_project()
        authors = load_authors_per_project(self.otherKedeGit.project_name, self.otherKedeGit._names_to_authors)
        self.assertEqual(len(authors), 1)
