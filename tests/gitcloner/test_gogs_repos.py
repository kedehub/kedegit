import unittest
from urllib.parse import urlparse
from kedehub.gitcloner.gogs_repos import GogsClient

HOST = 'http://git.elando.bg'
USER_NAME = 'dimitar.bakardzhiev'
TOKEN = '0670a7aa94afc74c587cbf856ea84c0383287308'

class GogsReposTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = GogsClient(HOST, TOKEN, USER_NAME)

    def test_get_user_repos(self):
        repos = self.client.get_repos()
        self.assertGreater(len(repos),1)

    def test_replace_repo_port(self):
        repos = self.client.get_repos()
        replaced_port_url = self.client.replace_port(repos[0])
        parsed_replaced_port_url = urlparse(replaced_port_url)
        self.assertEqual(None, parsed_replaced_port_url.port)


if __name__ == '__main__':
    unittest.main()
