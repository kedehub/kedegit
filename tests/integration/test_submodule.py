import os
import git
from git import rmtree
from tests.kedegit_test import KedeGitTest
from kedehub.services.commit_service import get_commits_per_project


class KedeGitSubmoduleTest(KedeGitTest):

    def setUp(self):
        super().setUp()
        self.cloned_worktree = os.path.join(self.working_directory.name, 'worktree')
        git.Repo.clone_from(os.path.join(self.current_directory, '../tests/data', 'repository'),
                            os.path.join(self.working_directory.name, 'worktree'))
        repository = git.Repo(self.cloned_worktree)
        git.Submodule.add(repository, 'subrepo', 'subrepo',
                          os.path.join(self.current_directory, '../tests/data', 'subrepository'))
        author = git.Actor('Author A', 'a@example.com')
        repository.index.commit('Add subrepo', author=author)

    def tearDown(self):
        rmtree(self.cloned_worktree)
        super().tearDown()

    def test_repository_with_added_submodule_is_understood(self):
        self.kedegit.add_repository(self.cloned_worktree)
        # To get the commit count across all branches:
        # git rev-list --all --count
        commits = get_commits_per_project(self.kedegit.project_name,
                                          self.kedegit._shas_to_commits)
        self.assertEqual(len(commits), 7)

    def test_submodule_in_initial_commit_is_understood(self):
        submodule_repository = git.Repo.init(os.path.join(self.working_directory.name, 'initial_submodule'))
        git.Submodule.add(submodule_repository, 'subrepo', 'subrepo',
                          os.path.join(self.current_directory, '../tests/data', 'subrepository'))
        author = git.Actor('Author B', 'b@example.com')
        submodule_repository.create_remote('origin','https://gitlab.com/Company_Name/submodule_repository_name.git')
        submodule_repository.index.commit('Initial commit', author=author)
        self.kedegit.add_repository(os.path.join(self.working_directory.name, 'initial_submodule'))
        commits = get_commits_per_project(self.kedegit.project_name,
                                          self.kedegit._shas_to_commits)
        self.assertEqual(4, commits[0].added_lines)
        self.assertEqual(179, commits[0].added_chars)
        self.assertEqual({'Other': 179}, commits[0].lang_count)
