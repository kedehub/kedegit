import sys
import unittest

if '..' not in sys.path:
    sys.path.insert(0, '..')

from kedehub.services.dro.identity_blacklist_dto import MatchingBlacklist
from kedehub.matching.exceptions import MatcherNotSupportedError
from kedehub.matching.matcher import IdentityMatcher, create_identity_matcher, match
from kedehub.matching import EmailMatcher, EmailNameMatcher


class TestCreateIdentityMatcher(unittest.TestCase):

    maxDiff = None

    def test_identity_matcher_instance(self):
        """Test if the factory function returns an identity matcher instance"""

        matcher = create_identity_matcher('default')
        self.assertIsInstance(matcher, IdentityMatcher)

        matcher = create_identity_matcher('email')
        self.assertIsInstance(matcher, EmailMatcher)

        matcher = create_identity_matcher('email-name')
        self.assertIsInstance(matcher, EmailNameMatcher)


    def test_identity_matcher_instance_with_blacklist(self):
        """Test if the factory function adds a blacklist to the matcher instance"""

        # The blacklist is empty
        matcher = create_identity_matcher('default')
        self.assertIsInstance(matcher, IdentityMatcher)
        self.assertEqual(len(matcher.blacklist), 0)

        # Create a matcher with a blacklist
        blacklist = [MatchingBlacklist(excluded='JSMITH@example.com'),
                     MatchingBlacklist(excluded='jrae@example.com'),
                     MatchingBlacklist(excluded='jrae@example.net'),
                     MatchingBlacklist(excluded='John Smith'),
                     MatchingBlacklist(excluded='root')]

        matcher = create_identity_matcher('default', blacklist=blacklist)
        self.assertIsInstance(matcher, IdentityMatcher)
        self.assertEqual(len(matcher.blacklist), 5)

    def test_identity_matcher_instance_with_sources_list(self):
        """Test if the factory function adds a sources list to the matcher instance"""

        # The sources list is None
        matcher = create_identity_matcher('default')
        self.assertIsInstance(matcher, IdentityMatcher)
        self.assertEqual(matcher.sources, None)

        # Create a matcher with a sources list
        sources = ['git', 'jira', 'github']

        matcher = create_identity_matcher('default', sources=sources)
        self.assertIsInstance(matcher, IdentityMatcher)
        self.assertEqual(len(matcher.sources), 3)

    def test_identity_matcher_instance_with_strict(self):
        """Test if the factory function adds the strict mode to the matcher instance"""

        matcher = create_identity_matcher('default')
        self.assertIsInstance(matcher, IdentityMatcher)
        self.assertEqual(matcher.strict, True)

        matcher = create_identity_matcher('default', strict=False)
        self.assertIsInstance(matcher, IdentityMatcher)
        self.assertEqual(matcher.strict, False)

    def test_not_supported_matcher(self):
        """Check if an exception is raised when the given matcher type is not supported"""

        self.assertRaises(MatcherNotSupportedError,
                          create_identity_matcher, 'custom')

if __name__ == "__main__":
    unittest.main()