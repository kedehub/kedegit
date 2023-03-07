import unittest

from kedehub.matching.idmatching.filtering import is_blacklisted_email, is_ignored_email, is_ignored_name


class FilteringTestCase(unittest.TestCase):
    def test_is_blacklisted_email_greenkeeper_bot(self):
        self.assertEqual(True, is_blacklisted_email('greenkeeper[bot]@users.noreply.github.com'))

    def test_is_blacklisted_email_phillipvannortwick_izumo_local(self):
        self.assertEqual(False, is_blacklisted_email('phillipvannortwick@izumo.local'))

    def test_is_ignored_email_phillipvannortwick_izumo_local(self):
        self.assertEqual(True, is_ignored_email('phillipvannortwick@izumo.local'))

    def test_is_ignored_email_greenkeeper_bot(self):
        self.assertEqual(True, is_ignored_email('greenkeeper[bot]@users.noreply.github.com'))

    def test_is_ignored_email_snyk_bot(self):
        self.assertEqual(True, is_ignored_email('admin+snyk-bot@snyk.io'))

    def test_is_ignored_email_jenkins_wendy(self):
        self.assertEqual(True, is_ignored_email('jenkins@wendy.feedhenry.net'))

    def test_is_ignored_email_jenkins_everbuild(self):
        self.assertEqual(True, is_ignored_email('jenkins@everbuild.feedhenry.net'))

    def test_is_ignored_name_jenkins(self):
        self.assertEqual(True, is_ignored_name('Jenkins'))

    def test_is_ignored_name_jenkins_small_case(self):
        self.assertEqual(True, is_ignored_name('jenkins'))

    def test_is_ignored_email_DonnaM_MacBook_Air_local(self):
        self.assertEqual(True, is_ignored_email('DonnaM@Donnas-MacBook-Air.local'))

    def test_is_ignored_email_shrishrirang_users_noreply_github_com(self):
        self.assertEqual(False, is_ignored_email('shrishrirang@users.noreply.github.com'))

    def test_is_ignored_email_shrishrirang_users_travis_org(self):
        self.assertEqual(True, is_ignored_email('shrishrirang@travis-ci.org'))


if __name__ == '__main__':
    unittest.main()
