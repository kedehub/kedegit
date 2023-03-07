import unittest

from kedehub.gitcloner.bitbucket_repos import BitbucketClient

WORKSPACE_ID = 'tallertechnologiesbulgaria'
USERNAME = 'dimitar_bakardzhiev'
PASSWORD = '9711324aA!'

class BitbucketReposTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = BitbucketClient(WORKSPACE_ID, USERNAME, PASSWORD)

    def test_get_repos(self):
        repos = self.client.get_repos()
        self.assertGreater(len(repos),1)


if __name__ == '__main__':
    unittest.main()
