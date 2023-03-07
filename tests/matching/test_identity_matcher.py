import sys
import unittest

if '..' not in sys.path:
    sys.path.insert(0, '..')

from kedehub.services.dro.identity_blacklist_dto import MatchingBlacklist
from kedehub.matching.matcher import IdentityMatcher



class TestIdentityMatcher(unittest.TestCase):
    """Test IdentityMatcher class"""

    def test_blacklist(self):
        """Test blacklist contents"""

        m = IdentityMatcher()
        self.assertListEqual(m.blacklist, [])

        m = IdentityMatcher(blacklist=[])
        self.assertListEqual(m.blacklist, [])

        blacklist = [MatchingBlacklist(excluded='JSMITH@example.com'),
                     MatchingBlacklist(excluded='jrae@example.com'),
                     MatchingBlacklist(excluded='jrae@example.net'),
                     MatchingBlacklist(excluded='John Smith'),
                     MatchingBlacklist(excluded='root')]

        m = IdentityMatcher(blacklist=blacklist)

        self.assertListEqual(m.blacklist, ['john smith', 'jrae@example.com',
                                           'jrae@example.net', 'jsmith@example.com',
                                           'root'])

    def test_sources_list(self):
        """Test sources list contents"""

        m = IdentityMatcher()
        self.assertEqual(m.sources, None)

        m = IdentityMatcher(sourecs=[])
        self.assertEqual(m.sources, None)

        sources = ['git', 'Jira', 'GitHub']
        m = IdentityMatcher(sources=sources)

        self.assertListEqual(m.sources, ['git', 'github', 'jira'])

    def test_strict_mode(self):
        """Test strict mode value"""

        m = IdentityMatcher()
        self.assertEqual(m.strict, True)

        m = IdentityMatcher(strict=False)
        self.assertEqual(m.strict, False)

if __name__ == "__main__":
    unittest.main()