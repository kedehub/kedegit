import sys
import unittest
from uuid import UUID

from kedehub.services.dro.user_dto import User

if '..' not in sys.path:
    sys.path.insert(0, '..')

from kedehub.services.dro.author_dto import Author

from kedehub.matching.matcher import match
from kedehub.matching import EmailMatcher, EmailNameMatcher

class TestMatch(unittest.TestCase):
    """Test match function"""
    maxDiff = None

    def setUp(self):
        # Add some unique identities

        self.john_smith = User(name= 'John Smith')
        self.john_smith.identities = [Author(canonical_name= 'John Smith <jsmith@google.com>', email='jsmith@google.com', name='John Smith',
                                               user_id=self.john_smith.id),
                                      Author(canonical_name= 'John Smith <>', email = '', name='John Smith',
                                               user_id=self.john_smith.id),
                                      Author(canonical_name= 'John Smith <jsmith@google.com>', email='jsmith@google.com', name='John Smith',
                                               user_id=self.john_smith.id)]

        self.jsmith = User(name= 'J. Smith')
        self.jsmith.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email = '',
                                           user_id=self.jsmith.id),
                                  Author(canonical_name='John Smith <>', name='John Smith', email = '',
                                           user_id=self.jsmith.id),
                                  Author(canonical_name=' <jsmith>', name='', email='jsmith',
                                           user_id=self.jsmith.id)]

        self.jane_rae = User(name= 'Jane Rae')
        self.jane_rae.identities = [Author(canonical_name= 'Janer Rae <>', name='Janer Rae', email = '',
                                             user_id=self.jane_rae.id),
                                    Author(canonical_name= 'Jane Rae Doe <jane.rae@google.net>', name='Jane Rae Doe', email='jane.rae@google.net',
                                             user_id=self.jane_rae.id)]

        self.js_alt = User(name= 'john_smith')
        self.js_alt.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email = '',
                                           user_id=self.js_alt.id),
                                  Author(canonical_name= ' <>', name='',email = '',
                                           user_id=self.js_alt.id),
                                  Author(canonical_name= ' <>', name='',email = '',
                                           user_id=self.js_alt.id),
                                  Author(canonical_name='Smith. J <JSmith@google.com>', email='JSmith@google.com', name='Smith. J',
                                            user_id=self.js_alt.id)]

        self.jrae = User(name= 'jrae')
        self.jrae.identities = [Author(canonical_name='Jane Rae Doe <jrae@google.net>', email='jrae@google.net', name='Jane Rae Doe',
                                         user_id=self.jrae.id),
                                Author(canonical_name='jrae <>', name='jrae', email='', source='mls', user_id=self.jrae.id),
                                Author(canonical_name='jrae <>', name='jrae', email='', source='scm', user_id=self.jrae.id)]

    def test_match_email_no_inout_users(self):
        """Test whether the function returns no matches matching using email matcher"""

        users = [self.jsmith, self.jrae, self.js_alt,
                       self.john_smith, self.jane_rae]

        matcher = EmailMatcher()

        result = match([], matcher)
        self.assertEqual(len(result), 0)

    def test_match_email(self):
        """Test whether the function finds every possible matching using email matcher"""

        users = [self.jsmith, self.jrae, self.js_alt,
                       self.john_smith, self.jane_rae]

        matcher = EmailMatcher()

        result = match(users, matcher)

        expected = [[self.john_smith, self.js_alt],
                   [self.jane_rae], [self.jrae], [self.jsmith]]

        self.assertEqual(len(result), 4)
        self.assertListEqual(result,
                             expected)

    def test_match_email_blacklisted_domain(self):
        """Test whether the function ignores blacklisted domain using email matcher
            Note: example.com is blacklisted
        """

        john_smith = User(name= 'John Smith')
        john_smith.identities = [Author(canonical_name= 'John Smith <jsmith@example.com>', email='jsmith@example.com', name='John Smith',
                                               user_id=john_smith.id),
                                      Author(canonical_name= 'John Smith <>', email = '', name='John Smith',
                                               user_id=john_smith.id),
                                      Author(canonical_name= 'John Smith <jsmith@example.com>', email='jsmith@example.com', name='John Smith',
                                               user_id=john_smith.id)]

        jsmith = User(name= 'J. Smith')
        jsmith.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email = '',
                                           user_id=jsmith.id),
                                  Author(canonical_name='John Smith <>', name='John Smith', email = '',
                                           user_id=jsmith.id),
                                  Author(canonical_name=' <jsmith>', name='', email='jsmith',
                                           user_id=jsmith.id)]

        jane_rae = User(name= 'Jane Rae')
        jane_rae.identities = [Author(canonical_name= 'Janer Rae <>', name='Janer Rae', email = '',
                                             user_id=jane_rae.id),
                                    Author(canonical_name= 'Jane Rae Doe <jane.rae@example.net>', name='Jane Rae Doe', email='jane.rae@example.net',
                                             user_id=jane_rae.id)]

        js_alt = User(name= 'john_smith')
        js_alt.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email = '',
                                           user_id=js_alt.id),
                                  Author(canonical_name= ' <>', name='',email = '',
                                           user_id=js_alt.id),
                                  Author(canonical_name= ' <>', name='',email = '',
                                           user_id=js_alt.id),
                                  Author(canonical_name='Smith. J <JSmith@example.com>', email='JSmith@example.com', name='Smith. J',
                                            user_id=js_alt.id)]

        jrae = User(name= 'jrae')
        jrae.identities = [Author(canonical_name='Jane Rae Doe <jrae@example.net>', email='jrae@example.net', name='Jane Rae Doe',
                                         user_id=jrae.id),
                                Author(canonical_name='jrae <>', name='jrae', email='', source='mls', user_id=jrae.id),
                                Author(canonical_name='jrae <>', name='jrae', email='', source='scm', user_id=jrae.id)]
        users = [jsmith, jrae, js_alt,
                       john_smith, jane_rae]

        matcher = EmailMatcher()

        result = match(users, matcher)

        expected = [[jane_rae], [jrae], [jsmith], [js_alt], [john_smith]]

        self.assertEqual(5, len(result))
        self.assertListEqual(expected, result)

    def test_match_email_name(self):
        """Test whether the function finds every possible matching using email-name matcher

            Note: jsmith has invalid email hence it is not considered
        """

        users = [self.jsmith, self.jrae, self.js_alt,
                       self.john_smith, self.jane_rae]

        matcher = EmailNameMatcher()

        result = match([], matcher)
        self.assertEqual(len(result), 0)

        result = match(users, matcher)

        self.assertEqual(3, len(result))
        self.assertListEqual([[self.jane_rae, self.jrae],
                             [self.john_smith, self.js_alt], [self.jsmith]],
                             result)

    def test_match_email_name_michael(self):
        """Test whether the function finds every possible matching using email-name matcher

            Note: 'michael' is a popular name hence it is not considered
        """

        Michael_Bannister = User(name='Michael Bannister')
        Michael_Bannister.identities = [Author(canonical_name='Michael Bannister <github@michaelbannister.co.uk>', aliases=None, name='Michael Bannister', email='github@michaelbannister.co.uk', user_id=Michael_Bannister.id)]

        michael = User(name='michael')
        michael.identities = [Author(canonical_name='michael <michael@localhost.localdomain>', aliases=None, name='michael', email='michael@localhost.localdomain', user_id=michael.id)]

        Michael_Wermeester = User(name='Michael Wermeester')
        Michael_Wermeester.identities = [Author(canonical_name='Michael Wermeester <michael.wermeester@me.com>', aliases=None, name='Michael Wermeester', email='michael.wermeester@me.com', user_id=Michael_Wermeester.id)]

        Michael_Pellegrini = User(name='Michael Pellegrini')
        Michael_Pellegrini.identities = [Author(canonical_name='Michael Pellegrini <mike.pellegrini@allegiantair.com>', aliases=None, name='Michael Pellegrini', email='mike.pellegrini@allegiantair.com', user_id=Michael_Pellegrini.id)]

        Michael_Musgrove = User(name='Michael Musgrove')
        Michael_Musgrove.identities = [Author(canonical_name='Michael Musgrove <mmusgrov@redhat.com>', aliases=None, name='Michael Musgrove', email='mmusgrov@redhat.com', user_id=Michael_Musgrove.id)]

        mmusgrov = User(name='mmusgrov')
        mmusgrov.identities = [Author(canonical_name='mmusgrov <mmusgrov@redhat.com>', aliases=None, name='mmusgrov', email='mmusgrov@redhat.com', user_id=mmusgrov.id)]

        Michael_Levin = User(name='Michael Levin')
        Michael_Levin.identities = [Author(canonical_name='Michael Levin <kinnetica@gmail.com>', aliases=None, name='Michael Levin', email='kinnetica@gmail.com', user_id=Michael_Levin.id)]

        Michael_Edgar = User(name='Michael Edgar')
        Michael_Edgar.identities = [Author(canonical_name='Michael Edgar <michael@xlate.io>', aliases=None, name='Michael Edgar', email='michael@xlate.io', user_id=Michael_Edgar.id)]

        users = [Michael_Bannister, michael, Michael_Wermeester,
                       Michael_Pellegrini, Michael_Musgrove, mmusgrov,
                 Michael_Levin, Michael_Edgar]

        matcher = EmailNameMatcher()

        result = match(users, matcher)

        self.assertEqual(7, len(result))
        self.assertListEqual(
                             [[Michael_Musgrove, mmusgrov],
                              [Michael_Edgar], [Michael_Levin], [Michael_Pellegrini], [Michael_Wermeester],[Michael_Bannister],[michael]],
                            result
                             )

    def test_match_email_name_no_michael(self):
        """Test whether the function finds every possible matching using email-name matcher
            Note: 'michael' is removed
        """

        Michael_Bannister = User(name='Michael Bannister')
        Michael_Bannister.identities = [Author(canonical_name='Michael Bannister <github@michaelbannister.co.uk>', aliases=None, name='Michael Bannister', email='github@michaelbannister.co.uk', user_id=Michael_Bannister.id)]

        # michael = User(name='michael')
        # michael.identities = [Author(canonical_name='michael <michael@localhost.localdomain>', aliases=None, name='michael', email='michael@localhost.localdomain', user_id=michael.id)]

        Michael_Wermeester = User(name='Michael Wermeester')
        Michael_Wermeester.identities = [Author(canonical_name='Michael Wermeester <michael.wermeester@me.com>', aliases=None, name='Michael Wermeester', email='michael.wermeester@me.com', user_id=Michael_Wermeester.id)]

        Michael_Pellegrini = User(name='Michael Pellegrini')
        Michael_Pellegrini.identities = [Author(canonical_name='Michael Pellegrini <mike.pellegrini@allegiantair.com>', aliases=None, name='Michael Pellegrini', email='mike.pellegrini@allegiantair.com', user_id=Michael_Pellegrini.id)]

        Michael_Musgrove = User(name='Michael Musgrove')
        Michael_Musgrove.identities = [Author(canonical_name='Michael Musgrove <mmusgrov@redhat.com>', aliases=None, name='Michael Musgrove', email='mmusgrov@redhat.com', user_id=Michael_Musgrove.id)]

        mmusgrov = User(name='mmusgrov')
        mmusgrov.identities = [Author(canonical_name='mmusgrov <mmusgrov@redhat.com>', aliases=None, name='mmusgrov', email='mmusgrov@redhat.com', user_id=mmusgrov.id)]

        Michael_Levin = User(name='Michael Levin')
        Michael_Levin.identities = [Author(canonical_name='Michael Levin <kinnetica@gmail.com>', aliases=None, name='Michael Levin', email='kinnetica@gmail.com', user_id=Michael_Levin.id)]

        Michael_Edgar = User(name='Michael Edgar')
        Michael_Edgar.identities = [Author(canonical_name='Michael Edgar <michael@xlate.io>', aliases=None, name='Michael Edgar', email='michael@xlate.io', user_id=Michael_Edgar.id)]

        users = [Michael_Bannister, Michael_Wermeester,
                       Michael_Pellegrini, Michael_Musgrove, mmusgrov,
                 Michael_Levin, Michael_Edgar]

        matcher = EmailNameMatcher()

        result = match(users, matcher)

        self.assertEqual(6, len(result))
        self.assertListEqual(
                             [[Michael_Musgrove, mmusgrov],
                              [Michael_Edgar], [Michael_Levin], [Michael_Pellegrini], [Michael_Wermeester],[Michael_Bannister]],
                            result
                             )

    def test_matcher_error(self):
        """Test if it raises an error when the matcher is not valid"""

        self.assertRaises(TypeError, match, [], None)
        self.assertRaises(TypeError, match, [], "")



if __name__ == "__main__":
    unittest.main()
