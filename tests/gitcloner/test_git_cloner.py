import unittest
from tests.kedegit_test import KedeGitTest
from kedehub.gitcloner.github_repos import GithubClient
from kedehub.utility.os_utils import create_folder
from tests import working_directory
from kedehub.gitcloner.git_cloner import GitCloner, clone_a_repo
from kedehub import server_config

TOKEN_GITHUB = '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'
ORG_GITHUB = 'facebook'

class GitClonerTestCase(KedeGitTest):

    def test_clone_all_github(self):
        client = GithubClient(TOKEN_GITHUB, ORG_GITHUB)
        cloner = GitCloner(working_directory.name, client)

        cloner.clone_all()

    def test_clone_repo_github(self):
        client = GithubClient(TOKEN_GITHUB, ORG_GITHUB)
        cloner = GitCloner(working_directory.name, client)
        self.assertTrue(cloner.clone_repo('https://github.com/facebook/codemod.git'))

    def test_clone_repo_github_folder_exixts(self):
        client = GithubClient(TOKEN_GITHUB, ORG_GITHUB)
        cloner = GitCloner(working_directory.name, client)
        create_folder(working_directory.name, 'codemod')
        self.assertIsNone(cloner.clone_repo('https://github.com/facebook/codemod.git'))

    def test_clone_repo_github_repo_exixts_in_config(self):
        client = GithubClient(TOKEN_GITHUB, ORG_GITHUB)
        cloner = GitCloner(working_directory.name, client)

        origin = 'http://git.test.com/test_company/test_repo.git'
        repository_path = '/Users/dimitarbakardzhiev/git/test_repo'
        configuration_file_path = '/Users/dimitarbakardzhiev/git/kedehub/kede-config.json'

        server_config.add_new_repo(origin, repository_path, configuration_file_path)

        self.assertIsNone(cloner.clone_repo('http://git.test.com/test_company/test_repo.git'))

    def test_clone_a_repo(self):
        forlder = 'codemod'
        clone_path = create_folder(working_directory.name, forlder)
        self.assertTrue(clone_a_repo(clone_path, 'https://github.com/facebook/codemod.git'))

if __name__ == '__main__':
    unittest.main()
