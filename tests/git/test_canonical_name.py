import unittest

from kedehub.git.git_utility import get_email, get_name


class KedeGitCanonicalNameTest(unittest.TestCase):
    def test_get_emal(self):
        email = get_email('Dimitar <dimitar>')
        self.assertEqual('dimitar', email)

    def test_get_name(self):
        name = get_name('Dimitar <dimitar>')
        self.assertEqual('Dimitar', name)

if __name__ == '__main__':
    unittest.main()
