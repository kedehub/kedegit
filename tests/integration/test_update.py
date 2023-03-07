import os
import git
from git import rmtree

from tests.kedegit_test import KedeGitTest
from kedehub.services.commit_service import get_commits_per_project, get_project_commits
from kedehub.services.author_service import load_authors_for_projects

NUMBER_COMMITS_MASTER_BRANCH = 6

NUMBER_COMMITS_OLD_STATE_BRANCH = 1


class KedeGitUpdateTest(KedeGitTest):

    def _update_from_old_state(self):
        self.git_repository.remote().fetch('+refs/heads/master:refs/remotes/origin/master')
        self.git_repository.create_head('master', self.git_repository.remote().refs.master)
        self.git_repository.heads.master.checkout()
        self.kedegit.update_data()

    def setUp(self):
        super().setUp()
        self.cloned_worktree = os.path.join(self.working_directory.name, 'worktree')
        self.git_repository = git.Repo.clone_from(os.path.join(self.current_directory, '../tests/data', 'repository'),
                                                  self.cloned_worktree,
                                                  branch='old-state', single_branch=True)
        self.kedegit.add_repository(self.cloned_worktree)

    def tearDown(self):
        rmtree(self.cloned_worktree)
        super().tearDown()

    def test_clone_produced_expected_result(self):
        commits = list(get_commits_per_project(self.kedegit.project_name,
                                               self.kedegit._shas_to_commits))
        self.assertEqual(NUMBER_COMMITS_OLD_STATE_BRANCH, len(commits))
        self.assertEqual(commits[0].hexsha, KedeGitUpdateTest._main_repo_initial_commit_hexsha)
        initial_commit = self._fetch_commit(KedeGitUpdateTest._main_repo_initial_commit_hexsha)
        self.assertIn(initial_commit.author_name, commits[0].author_name)
        self.assertEqual(14, commits[0].added_lines)
        self.assertEqual({'Text': 17}, commits[0].lang_count)

        expected = ['Author A <a@example.com>']
        persons = load_authors_for_projects([self.kedegit.project_name])
        self.assertEqual(expected, persons)

    def test_updating_project_does_not_add_new_commits(self):
        self.kedegit.update_data()
        commits = list(get_project_commits(self.kedegit.project_name))
        self.assertEqual(NUMBER_COMMITS_OLD_STATE_BRANCH, len(commits))

        expected = ['Author A <a@example.com>']
        persons = load_authors_for_projects([self.kedegit.project_name])
        self.assertEqual(expected, persons)

    def test_updating_project_after_repository_updated_brings_in_new_commits(self):
        self._update_from_old_state()
        commits = list(get_commits_per_project(self.kedegit.project_name,
                                               self.kedegit._shas_to_commits))
        self.assertEqual(NUMBER_COMMITS_MASTER_BRANCH, len(commits))
        self.assertEqual(commits[0].hexsha, KedeGitUpdateTest._main_repo_initial_commit_hexsha)
        self.assertEqual(commits[1].hexsha, KedeGitUpdateTest._main_repo_second_commit_hexsha)
        initial_commit = self._fetch_commit(KedeGitUpdateTest._main_repo_initial_commit_hexsha)
        second_commit = self._fetch_commit(KedeGitUpdateTest._main_repo_second_commit_hexsha)
        self.assertEqual(initial_commit.added_lines, 14)
        self.assertEqual(second_commit.added_lines, 4)
        self.assertEqual({'Text': 4}, second_commit.lang_count)

        expected = ['Author A <a@example.com>',
                     'Author B <b@example.com>',
                     'Author C <c@example.com>']
        persons = load_authors_for_projects([self.kedegit.project_name])
        self.assertEqual(expected, persons)
