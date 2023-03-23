import os
import git
from git import rmtree
from tests.kedegit_test import KedeGitTest
from kedehub.services.commit_service import get_commits_per_project


class KedeGitShallowTest(KedeGitTest):
    def setUp(self):
        super().setUp()
        self.cloned_worktree = os.path.join(self.working_directory.name, 'worktree')
        self.git_repository = git.Repo.clone_from('file://' + os.path.join(self.current_directory, '../tests/data', 'repository'),
                                                  self.cloned_worktree,
                                                  depth=1)
        self.kedegit.add_repository(self.cloned_worktree,
                                    os.path.join(self.current_directory, '../tests/data', 'repo-config.json'))

    def tearDown(self):
        rmtree(self.cloned_worktree)
        super().tearDown()

    def test_shallow_clone_has_only_one_commit(self):
        commits = list(get_commits_per_project(self.kedegit.project_name,
                                               self.kedegit._shas_to_commits))
        self.assertEqual(1, len(commits))

    def test_shallow_clone_has_correct_counts(self):
        commit = self._fetch_commit(KedeGitShallowTest._main_repo_head_commit_hexsha)
        added_lines = commit.added_lines
        self.assertEqual(0, added_lines)
