import unittest

from kedehub.gitcloner.github_repos import GithubClient

TOKEN = '325103ac88ae8a937be2aef635bcd194696b6d0a'
ORG = 'facebook'

class GithubReposTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = GithubClient(TOKEN, ORG)

    def test_get_repos(self):
        repos = self.client.get_repos()
        self.assertGreater(len(repos), 1)

        self.assertEqual('https://github.com/facebook/hhvm.git', repos[1])





if __name__ == '__main__':
    unittest.main()
