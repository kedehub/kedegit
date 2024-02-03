import os
import unittest

from kedehub.gitclient.git_utility import get_git_repository, get_repository_remote_origin_url


class KedeGitRemoteRepoTestCase(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.abspath(os.path.dirname(__file__))

    def test_get_remote_show_origin(self):
        repository_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos')
        brepo = get_git_repository(repository_path)

        remoteUrl = get_repository_remote_origin_url(brepo)
        self.assertEqual('http://git.elando.bg/eLando/azbg_virtual_pos.git', remoteUrl)

    def test_non_existig_remote_origin(self):
        repository_path = os.path.join(self.current_directory, '../data', 'no_repote_in_repo_dir')
        brepo = get_git_repository(repository_path)

        with self.assertRaises(ValueError) as cm:
            get_repository_remote_origin_url(brepo)
        self.assertMultiLineEqual("Remote named \'origin\' didn\'t exist", str(cm.exception))

    def test_non_existig_repo_in_dir(self):
        repository_path = os.path.join(self.current_directory, '../data', 'non_repo_dir')

        brepo = get_git_repository(repository_path)

        self.assertIsNone(brepo)

    def test_existig_repo_in_dir(self):
        repository_path = os.path.join(self.current_directory, '../data', 'repository')

        brepo = get_git_repository(repository_path)

        self.assertIsNotNone(brepo)

if __name__ == '__main__':
    unittest.main()
