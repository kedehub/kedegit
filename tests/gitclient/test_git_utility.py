import unittest

from kedehub.gitclient.git_utility import get_repo_name


class KedeGitUtilityTest(unittest.TestCase):
    def test_get_repo_name(self):
        url = "https://github.com/apache/servicemix.git"

        project_name = get_repo_name(url)

        self.assertEqual('servicemix', project_name)

    def test_get_repo_name_no_dot_git_at_the_aned(self):
        url = "https://github.com/apache/servicemix"

        project_name = get_repo_name(url)

        self.assertEqual('servicemix', project_name)

if __name__ == '__main__':
    unittest.main()
