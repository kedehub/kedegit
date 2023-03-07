import sys
import unittest

from kedehub.services.dro.author_dto import Author
from kedehub.services.dro.identity_blacklist_dto import MatchingBlacklist
from kedehub.services.dro.user_dto import User

if '..' not in sys.path:
    sys.path.insert(0, '..')

from kedehub.matching.email import EmailMatcher, EmailIdentity


class TestEmailMatcher(unittest.TestCase):

    def test_match(self):
        """Test match method"""

        # Let's define some identities first
        jsmith = User(name='jsmith')
        jsmith.identities = [Author(canonical_name= 'John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='ohn Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        john_smith = User(name='js')
        john_smith.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email='', user_id=john_smith.id),
                                 Author(canonical_name=' <>', name='', email='', user_id=john_smith.id),
                                 Author(canonical_name='Smith. J <>', name='Smith. J', email='', user_id=john_smith.id),
                                 Author(canonical_name='Smith. J <JSmith@google.com>', name='Smith. J', email='JSmith@google.com', user_id=john_smith.id)]

        jsmith_alt = User(name='J. Smith')
        jsmith_alt.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <>', name='', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <jsmith>', name='', email='jsmith', user_id=jsmith_alt.id)]

        jsmith_not_email = User(name='John Smith')
        jsmith_not_email.identities = [Author(canonical_name=' <jsmith>', name='', email='jsmith', user_id=jsmith_not_email.id)]

        # Tests
        matcher = EmailMatcher()

        # First two unique identities must match
        result = matcher.match(jsmith, john_smith)
        self.assertEqual(result, True)

        result = matcher.match(john_smith, jsmith)
        self.assertEqual(result, True)

        # Comparing with the third does not produce any match
        result = matcher.match(jsmith, jsmith_alt)
        self.assertEqual(result, False)

        result = matcher.match(jsmith_alt, jsmith)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jsmith_alt)
        self.assertEqual(result, False)

        result = matcher.match(jsmith_alt, john_smith)
        self.assertEqual(result, False)

        # This two unique identities have the same email address
        # but due to 'jsmith' is not a valid email address, they
        # do not match
        result = matcher.match(jsmith_alt, jsmith_not_email)
        self.assertEqual(result, False)

    def test_match_with_blacklist(self):
        """Test match when there are entries in the blacklist"""

        # Let's define some identities first
        jsmith = User(name='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        john_smith = User(name='js')
        john_smith.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email='', user_id=john_smith.id),
                                 Author(canonical_name=' <>', name='', email='', user_id=john_smith.id),
                                 Author(canonical_name='Smith. J <>', name='Smith. J', email='', user_id=john_smith.id),
                                 Author(canonical_name='Smith. J <JSmith@google.com>', name='Smith. J', email='JSmith@google.com', user_id=john_smith.id)]

        jrae = User(name='jrae')
        jrae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jrae.id),
                           Author(canonical_name='Jane Rae Doe <jane.rae@google.net>', name='Jane Rae Doe', email='jane.rae@google.net', user_id=jrae.id),
                           Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae.id),
                           Author(canonical_name=' <JRAE@google.net>', name='', email='JRAE@google.net', user_id=jrae.id)]

        jane_rae = User(name='Jane Rae')
        jane_rae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jane_rae.id),
                               Author(canonical_name='  <jrae@google.net>',  name='', email='jrae@google.net', user_id=jane_rae.id)]

        # Check matching
        matcher = EmailMatcher()

        # First two unique identities must match
        result = matcher.match(jsmith, john_smith)
        self.assertEqual(result, True)

        result = matcher.match(john_smith, jsmith)
        self.assertEqual(result, True)

        result = matcher.match(jrae, jane_rae)
        self.assertEqual(result, True)

        result = matcher.match(jane_rae, jrae)
        self.assertEqual(result, True)

        # Add a blacklist
        bl = [MatchingBlacklist(excluded='Jsmith@google.com'),
              MatchingBlacklist(excluded='jrae@google.com')]

        matcher = EmailMatcher(blacklist=bl)

        result = matcher.match(jsmith, john_smith)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jsmith)
        self.assertEqual(result, False)

        result = matcher.match(jrae, jane_rae)
        self.assertEqual(result, True)

        result = matcher.match(jane_rae, jrae)
        self.assertEqual(result, True)

        # In this case, no match will be found
        bl = [MatchingBlacklist(excluded='Jsmith@google.com'),
              MatchingBlacklist(excluded='jrae@google.com'),
              MatchingBlacklist(excluded='jrae@google.net')]

        matcher = EmailMatcher(blacklist=bl)

        result = matcher.match(jsmith, john_smith)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jsmith)
        self.assertEqual(result, False)

        result = matcher.match(jrae, jane_rae)
        self.assertEqual(result, False)

        result = matcher.match(jane_rae, jrae)
        self.assertEqual(result, False)

    def test_match_no_mathch(self):
        """Test match when a list of sources to filter is given"""

        jsmith = User(name='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith1@google.com>', name='John Smith', email='jsmith1@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        jsmith_alt = User(name='J. Smith')
        jsmith_alt.identities = [Author(canonical_name='John Smith JR <jsmith@google.com>', name='John Smith JR', email='jsmith@google.com', user_id=jsmith_alt.id),
                                 Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <>', name='', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <jsmith>',  name='', email='jsmith', user_id=jsmith_alt.id)]


        matcher = EmailMatcher()
        result = matcher.match(jsmith, jsmith_alt)
        self.assertEqual(result, False)

    def test_match_same_identity(self):
        """Test whether there is a match comparing the same identity"""

        uid = User(name='John Smith')

        matcher = EmailMatcher()
        result = matcher.match(uid, uid)

        self.assertEqual(result, True)

    def test_match_same_uuid(self):
        """Test if there is a match when compares identities with the same UUID"""

        uid1 = User(id='d8bb2470-595f-4cef-9d3c-b2b016dd7625', name='John Smith')
        uid2 = User(id='d8bb2470-595f-4cef-9d3c-b2b016dd7625', name='John Smith')

        matcher = EmailMatcher()

        result = matcher.match(uid1, uid2)
        self.assertEqual(result, True)

        result = matcher.match(uid2, uid1)
        self.assertEqual(result, True)

        uid1 = User(id=None)
        uid2 = User(id=None)

        result = matcher.match(uid1, uid2)
        self.assertEqual(result, False)

    def test_match_identities_instances(self):
        """Test whether it raises an error when ids are not UniqueIdentities"""

        uid = User(name='John Smith')

        matcher = EmailMatcher()

        self.assertRaises(ValueError, matcher.match, 'John Smith', uid)
        self.assertRaises(ValueError, matcher.match, uid, 'John Smith')
        self.assertRaises(ValueError, matcher.match, None, uid)
        self.assertRaises(ValueError, matcher.match, uid, None)
        self.assertRaises(ValueError, matcher.match, 'John Smith', 'John Doe')

    def test_match_filtered_identities(self):
        """Test whether filtered identities match"""

        jsmith = EmailIdentity('1', None, 'jsmith@google.com')
        jsmith_alt = EmailIdentity('2', 'jsmith', 'jsmith@google.com')
        jsmith_uuid = EmailIdentity('3', 'jsmith', 'john.smith@google.com')

        matcher = EmailMatcher()

        result = matcher.match_filtered_identities(jsmith, jsmith_alt)
        self.assertEqual(result, True)

        result = matcher.match_filtered_identities(jsmith, jsmith_uuid)
        self.assertEqual(result, False)

        result = matcher.match_filtered_identities(jsmith_alt, jsmith)
        self.assertEqual(result, True)

        result = matcher.match_filtered_identities(jsmith_alt, jsmith_uuid)
        self.assertEqual(result, True)

        result = matcher.match_filtered_identities(jsmith_uuid, jsmith)
        self.assertEqual(result, False)

        result = matcher.match_filtered_identities(jsmith_uuid, jsmith_alt)
        self.assertEqual(result, True)

    def test_match_filtered_identities_with_blacklist(self):
        """Test whether filtered identities match when there is a blacklist"""

        jsmith = EmailIdentity('1', None, 'jsmith@google.com')
        jsmith_alt = EmailIdentity('2', 'jsmith', 'jsmith@google.com')
        jsmith_uuid = EmailIdentity('3', 'jsmith', 'john.smith@google.com')
        john_alt = EmailIdentity('4', None, 'john.smith@google.com')
        jsmith_none = EmailIdentity('4', 'john.smith@google.com', None)
        jdoe_none = EmailIdentity('4', 'jdoe@google.com', None)

        bl = [MatchingBlacklist(excluded='JSMITH@google.com')]

        matcher = EmailMatcher(blacklist=bl)

        result = matcher.match_filtered_identities(jsmith, jsmith_alt)
        self.assertEqual(result, False)

        result = matcher.match_filtered_identities(jsmith, jsmith_uuid)
        self.assertEqual(result, False)

        result = matcher.match_filtered_identities(jsmith_alt, jsmith)
        self.assertEqual(result, False)

        # Same UUID
        result = matcher.match_filtered_identities(jsmith_alt, jsmith_uuid)
        self.assertEqual(result, True)

        result = matcher.match_filtered_identities(jsmith_uuid, jsmith)
        self.assertEqual(result, False)

        # Same UUID
        result = matcher.match_filtered_identities(jsmith_uuid, jsmith_alt)
        self.assertEqual(result, True)

        result = matcher.match_filtered_identities(jsmith_uuid, john_alt)
        self.assertEqual(result, True)

        result = matcher.match_filtered_identities(john_alt, jsmith_uuid)
        self.assertEqual(result, True)

        # Although the UUID is equal to None, these two does not match
        result = matcher.match_filtered_identities(jsmith_none, jdoe_none)
        self.assertEqual(result, False)

    def test_match_filtered_identities_instances(self):
        """Test whether it raises an error when ids are not EmailNameIdentities"""

        fid = EmailIdentity('1 <>', None, 'jsmith@example.com')

        matcher = EmailMatcher()

        self.assertRaises(ValueError, matcher.match_filtered_identities, 'John Smith', fid)
        self.assertRaises(ValueError, matcher.match_filtered_identities, fid, 'John Smith')
        self.assertRaises(ValueError, matcher.match_filtered_identities, None, fid)
        self.assertRaises(ValueError, matcher.match_filtered_identities, fid, None)
        self.assertRaises(ValueError, matcher.match_filtered_identities, 'John Smith', 'John Doe')

    def test_filter_identities(self):
        """Test if identities are filtered"""

        # Let's define some identities first
        jsmith = User(uuid='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id),
                             Author(canonical_name=' <jsmith@test>', name='', email='jsmith@test', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        jrae = User(uuid='jrae')
        jrae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jrae.id),
                           Author(canonical_name='Jane Rae Doe <jane.rae@example.net>', name='Jane Rae Doe', email='jane.rae@example.net', user_id=jrae.id),
                           Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae.id),
                           Author(canonical_name=' <JRAE@example.net>', name='', email='JRAE@example.net', user_id=jrae.id)]

        matcher = EmailMatcher()

        result = matcher.filter(jsmith)
        self.assertEqual(len(result), 1)

        fid = result[0]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jsmith.id)
        self.assertEqual(fid.email, 'jsmith@google.com')

        result = matcher.filter(jrae)
        self.assertEqual(len(result), 2)

        fid = result[0]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jrae.id)
        self.assertEqual(fid.email, 'jane.rae@example.net')

        fid = result[1]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jrae.id)
        self.assertEqual(fid.email, 'jrae@example.net')

    def test_filter_identities_with_blacklist(self):
        """Test if identities are filtered when there is a blacklist"""

        # Let's define some identities first
        jsmith = User(uuid='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id),
                             Author(canonical_name=' <jsmith@test>', name='', email='jsmith@test', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        jrae = User(uuid='jrae')
        jrae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jrae.id),
                           Author(canonical_name='Jane Rae Doe <jane.rae@google.net>', name='Jane Rae Doe', email='jane.rae@google.net', user_id=jrae.id),
                           Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae.id),
                           Author(canonical_name=' <JRAE@google.net>', name='', email='JRAE@google.net', user_id=jrae.id)]

        bl = [MatchingBlacklist(excluded='jrae@google.net')]

        matcher = EmailMatcher(blacklist=bl)

        result = matcher.filter(jsmith)
        self.assertEqual(len(result), 1)

        fid = result[0]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jsmith.id)
        self.assertEqual(fid.email, 'jsmith@google.com')

        result = matcher.filter(jrae)
        self.assertEqual(1, len(result))

        fid = result[0]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jrae.id)
        self.assertEqual(fid.email, 'jane.rae@google.net')

    def test_filter_users(self):
        """Test if identities are filtered when there is a sources list"""

        # Let's define some identities first
        jsmith = User(uuid='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id),
                             Author(canonical_name=' <jsmith@test>', name='', email='jsmith@test', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        jrae = User(uuid='jrae')
        jrae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jrae.id),
                           Author(canonical_name='Jane Rae Doe <jane.rae@google.net>', name='Jane Rae Doe', email='jane.rae@google.net', user_id=jrae.id),
                           Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae.id),
                           Author(canonical_name=' <JRAE@google.net>', name='', email='JRAE@google.net', user_id=jrae.id)]

        # Tests
        matcher = EmailMatcher()

        result = matcher.filter(jsmith)
        self.assertEqual(len(result), 1)

        result = matcher.filter(jrae)
        self.assertEqual(len(result), 2)

        fid = result[0]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jrae.id)
        self.assertEqual(fid.email, 'jane.rae@google.net')

    def test_filter_identities_instances(self):
        """Test whether it raises an error when id is not a UniqueIdentity"""

        matcher = EmailMatcher()

        self.assertRaises(ValueError, matcher.filter, 'John Smith')
        self.assertRaises(ValueError, matcher.filter, None)

    def test_matching_criteria(self):
        """Test whether it returns the matching criteria keys"""

        criteria = EmailMatcher.matching_criteria()

        self.assertListEqual(criteria, ['email'])

    def test_filter_identities_with_domains_blacklist(self):
        """Test if identities are filtered when there is a blacklist"""

        # Let's define some identities first
        jsmith = User(uuid='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id),
                             Author(canonical_name=' <jsmith@travis-ci.org>', name='', email='jsmith@travis-ci.org', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        jrae = User(uuid='jrae')
        jrae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jrae.id),
                           Author(canonical_name='Jane Rae Doe <jane.rae@google.net>', name='Jane Rae Doe', email='jane.rae@google.net', user_id=jrae.id),
                           Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae.id),
                           Author(canonical_name=' <JRAE@travis-ci.org>', name='', email='JRAE@travis-ci.org', user_id=jrae.id)]

        matcher = EmailMatcher()

        result = matcher.filter(jsmith)
        self.assertEqual(len(result), 1)

        fid = result[0]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jsmith.id)
        self.assertEqual(fid.email, 'jsmith@google.com')

        result = matcher.filter(jrae)
        self.assertEqual(1, len(result))

        fid = result[0]
        self.assertIsInstance(fid, EmailIdentity)
        self.assertEqual(fid.user_id, jrae.id)
        self.assertEqual(fid.email, 'jane.rae@google.net')



if __name__ == "__main__":
    unittest.main()
