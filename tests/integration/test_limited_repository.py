import os
import git
from git import rmtree
from tests.kedegit_test import KedeGitTest
from kedehub.services.commit_service import get_project_commits

NUMBER_COMMITS_FEATURE_BRANCH = 4

NUMBER_COMMITS_MASTER_BRANCH = 6

class KedeGitLimitedTest(KedeGitTest):
    def setUp(self):
        super().setUp()
        self.cloned_worktree_dir = os.path.join(self.working_directory.name, 'worktree')
        self.start_date = None
        self.git_repository = git.Repo.clone_from(os.path.join(self.current_directory, '../tests/data', 'repository'),
                                             self.cloned_worktree_dir,
                                             branch='feature', single_branch=True)
        self.kedegit.add_repository(self.cloned_worktree_dir,
                                     earliest_date=self.start_date)

    def tearDown(self):
        super().tearDown()

    def test_updating_with_master_after_an_older_unmerged_branch_brings_in_plder_commits(self):
        """
        git branch --merged master
            december
              feature
            * master
              old-state
        git branch --merged december
            december
            old - state
        git branch --merged feature
            feature
            old - state
        """
        initial_commits = list(get_project_commits(self.kedegit.project_name))
        self.assertEqual(NUMBER_COMMITS_FEATURE_BRANCH, len(initial_commits))

        self.git_repository.remote().fetch('+refs/heads/master:refs/remotes/origin/master')
        self.git_repository.create_head('master', self.git_repository.remote().refs.master)
        self.git_repository.heads.master.checkout()

        other_kedegit = self._make_kedegit('test')
        other_kedegit.update_data()
        updated_commits = list(get_project_commits(other_kedegit.project_name))
        self.assertEqual(NUMBER_COMMITS_MASTER_BRANCH, len(updated_commits))
        rmtree(self.cloned_worktree_dir)

    def test_updating_with_a_branch_from_an_older_unmerged_branch_brings_in_plder_commits(self):
        """
        feature is a branch of december as can be seen using:
            git log --all --decorate --oneline --graph
        feature is not merged in december as can be seen suing:
            git branch --merged december
                december
                old - state
            git branch --merged feature
                feature
                old - state
        feature has one commit AFTER december as can be seen using:
            git log
                commit c80ee8a32baaee8df8133b8afca26d63d857684e (december)
                    Author: Author C <c@example.com>
                    Date:   Fri Jan 5 18:22:33 2018 +0700
                commit 10247c3a05e4bd35d827ed527a0aed39990338ea (feature)
                    Author: Author B <b@example.com>
                    Date:   Sat Jan 6 13:13:13 2018 +0200:
        """

        initial_commits = list(get_project_commits(self.kedegit.project_name))
        self.assertEqual(NUMBER_COMMITS_FEATURE_BRANCH, len(initial_commits))

        self.git_repository.remote().fetch('+refs/heads/december:refs/remotes/origin/december')
        self.git_repository.create_head('december', self.git_repository.remote().refs.december)
        self.git_repository.heads.december.checkout()

        other_kedegit = self._make_kedegit('test')
        other_kedegit.update_data()
        updated_commits = list(get_project_commits(other_kedegit.project_name))
        self.assertEqual(5, len(updated_commits))
        rmtree(self.cloned_worktree_dir)