import unittest
from tests.kedegit_test import KedeGitTest
from kedehub.gitcloner.bitbucket_repos import BitbucketClient
from kedehub.gitcloner.github_repos import GithubClient
from kedehub.gitcloner.gitlab_repos import GitlabClient
from kedehub.utility.os_utils import create_folder
from tests import working_directory
from kedehub.gitcloner.git_cloner import GitCloner, clone_a_repo
from kedehub.gitcloner.gogs_repos import GogsClient
from kedehub import server_config

HOST_GOGS = 'http://git.elando.bg'
USER_NAME_GOGS = 'dimitar.bakardzhiev'
TOKEN_GOGS = '0670a7aa94afc74c587cbf856ea84c0383287308'

TOKEN_GITHUB = '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'
ORG_GITHUB = 'facebook'

HOST_GITLAB = 'https://cisl.allianz.at/git/'
TOKEN_GITLAB = '3v5Qnqx61Lnn1GtxRZzB'

WORKSPACE_ID_BITBUCKET = 'tallertechnologiesbulgaria'
USER_NAME_BITBUCKET = 'dimitar_bakardzhiev'
PASSWORD_BITBUCKET = '9711324aA!'

class GitClonerTestCase(KedeGitTest):
    def test_clone_all_gogs(self):
        client = GogsClient(HOST_GOGS, TOKEN_GOGS, USER_NAME_GOGS)
        cloner = GitCloner(working_directory.name, client)

        cloner.clone_all()

    def test_clone_repo_gogs(self):
        client = GogsClient(HOST_GOGS, TOKEN_GOGS, USER_NAME_GOGS)
        cloner = GitCloner(working_directory.name, client)

        self.assertTrue(cloner.clone_repo('http://git.elando.bg/eLando/PMT4NIIS.git'))

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

    def test_clone_all_gitlab(self):
        client = GitlabClient(HOST_GITLAB ,TOKEN_GITLAB)
        cloner = GitCloner(working_directory.name, client)

        cloner.clone_all()

    def test_clone_repo_gitlab(self):
        client = GitlabClient(HOST_GITLAB ,TOKEN_GITLAB)
        cloner = GitCloner(working_directory.name, client)

        self.assertTrue(cloner.clone_repo('https://cisl.allianz.at/git/cisl-ext/ext-bulgaria.git'))

    def test_clone_all_bitbucket(self):
        client = BitbucketClient(WORKSPACE_ID_BITBUCKET, USER_NAME_BITBUCKET, PASSWORD_BITBUCKET)
        cloner = GitCloner(working_directory.name, client)

        cloner.clone_all()

    def test_clone_repo_bitbucket(self):
        client = BitbucketClient(WORKSPACE_ID_BITBUCKET, USER_NAME_BITBUCKET, PASSWORD_BITBUCKET)
        cloner = GitCloner(working_directory.name, client)

        self.assertTrue(cloner.clone_repo('https://dimitar_bakardzhiev@bitbucket.org/tallertechnologiesbulgaria/esp.git'))

    def test_clone_a_repo(self):
        forlder = 'codemod'
        clone_path = create_folder(working_directory.name, forlder)
        self.assertTrue(clone_a_repo(clone_path, 'https://github.com/facebook/codemod.git'))

if __name__ == '__main__':
    unittest.main()
