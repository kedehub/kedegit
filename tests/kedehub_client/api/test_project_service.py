import os
import unittest

from tests.kedegit_test import KedeGitTest
from kedehub.services.dro.project_dto import Project
from kedehub.services.dro.project_repository_dto import ProjectRepository
from kedehub.services.project_service import assign_new_repo_to_existing_project, ensure_project_exists, load_all_project_names
from kedehub_client.exceptions import UnexpectedResponse

class KedeHubProjectServiceTest(KedeGitTest):

    def setUp(self):
        super().setUp()
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'repository'))

    def tearDown(self):
        super().tearDown()

    def test_assign_existing_repo_to_non_existing_project(self):
        project_repository = ProjectRepository(
                                  project_name = 'test_2',
                                  repository_id = 2)

        with self.assertRaises(UnexpectedResponse):
            assign_new_repo_to_existing_project(project_repository.project_name, project_repository.repository_id)


    def test_assign_existing_repo_to_existing_project(self):
        project = Project(project_name='test_2',
                          company_name='test_company')
        new_project = ensure_project_exists(project.project_name)

        project_repository = ProjectRepository(
                                  project_name = new_project.project_name,
                                  repository_id = 1)
        new_project_repository = assign_new_repo_to_existing_project(project_repository.project_name, project_repository.repository_id)

        self.assertEqual(project_repository, new_project_repository)

    def test_assign_non_existing_repo_to_existing_project(self):
        project_repository = ProjectRepository(
                                  project_name = 'test',
                                  repository_id = 300)

        new_project_repository = assign_new_repo_to_existing_project(project_repository.project_name,
                                            project_repository.repository_id)

        self.assertIsNone(new_project_repository)


    def test_save_new_project(self):
        project = Project(project_name = 'test_2',
                          company_name='test_company')
        new_project = ensure_project_exists(project.project_name)

        self.assertEqual('test_2', new_project.long_name)
        self.assertEqual('test_2', new_project.project_name)
        self.assertEqual('test_company', new_project.company_name)

    def test_save_new_project_make_lower_case(self):
        project = Project(project_name = 'Test_2',
                          company_name = 'test_company')
        new_project = ensure_project_exists(project.project_name)

        self.assertEqual('Test_2', new_project.long_name)
        self.assertEqual('test_2', new_project.project_name)
        self.assertEqual('test_company', new_project.company_name)

    def test_save_new_project_name_with_space(self):
        project = Project(project_name = 'test 2',
                          company_name = 'test_company')
        new_project = ensure_project_exists(project.project_name)

        self.assertEqual('test 2', new_project.long_name)
        self.assertEqual('test_2', new_project.project_name)
        self.assertEqual('test_company', new_project.company_name)

    def test_not_saved_existing_project(self):
        project = Project(project_name = 'test',
                          company_name='test_company')
        new_project = ensure_project_exists(project.project_name)

        self.assertEqual('test', new_project.long_name)
        self.assertEqual('test', new_project.project_name)
        self.assertEqual('test_company', new_project.company_name)

    def test_get_all_projects(self):
        expected_project_names = ['test']
        project_names = load_all_project_names()
        self.assertListEqual(expected_project_names,project_names)


if __name__ == '__main__':
    unittest.main()
