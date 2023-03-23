import os
import unittest
import git

class KedeGitLogTestCase(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.abspath(os.path.dirname(__file__))

    def test_get_log(self):
        repository_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos')
        brepo = git.Repo(repository_path)

        author_lines = brepo.git.log(all=True, format='%aN <%aE>')
        self.assertEqual(4977, len(author_lines))


if __name__ == '__main__':
    unittest.main()
