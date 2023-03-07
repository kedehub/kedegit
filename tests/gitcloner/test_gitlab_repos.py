import unittest

from kedehub.gitcloner.gitlab_repos import GitlabClient

HOST = 'https://cisl.allianz.at/git/'
TOKEN = '3v5Qnqx61Lnn1GtxRZzB'

class GitlabReposCase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = GitlabClient(HOST, TOKEN)

    def test_get_gitlab_org_repos(self):
        repos = self.client.get_repos()
        self.assertGreater(len(repos), 1)


if __name__ == '__main__':
    unittest.main()
