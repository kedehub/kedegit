import sys
import unittest
from uuid import UUID

from kedehub.services.dro.author_dto import Author
from kedehub.services.dro.user_dto import User

if '..' not in sys.path:
    sys.path.insert(0, '..')

from kedehub.services.dro.identity_blacklist_dto import MatchingBlacklist
from kedehub.matching.email_name import EmailNameMatcher, EmailNameIdentity


class TestEmailNameMatcher(unittest.TestCase):

    def test_match(self):
        """Test match method"""

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

        jsmith_alt = User(name='J. Smith')
        jsmith_alt.identities = [Author(canonical_name='J. Smith <>', name='J. Smith', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <>', name='', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <jsmith>', name='', email='jsmith', user_id=jsmith_alt.id)]

        jsmith_not_email = User(name='John Smith')
        jsmith_not_email.identities = [Author(canonical_name='', name='', email='jsmith', user_id=jsmith_not_email.id)]

        jrae = User(name='jrae')
        jrae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jrae.id),
                           Author(canonical_name='Jane Rae Doe <jane.rae@google.net>', name='Jane Rae Doe', email='jane.rae@google.net', user_id=jrae.id)]

        jrae_doe = User(name='jraedoe')
        jrae_doe.identities = [Author(canonical_name='Jane Rae Doe <jrae@google.com>', name='Jane Rae Doe', email='jrae@google.com', user_id=jrae_doe.id),
                               Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae_doe.id)]

        jrae_no_name = User(name='Jane Rae')
        jrae_no_name.identities = [Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae_no_name.id)]

        # Tests
        matcher = EmailNameMatcher()

        # First two unique identities must match
        result = matcher.match(jsmith, john_smith)
        self.assertEqual(result, True)

        result = matcher.match(john_smith, jsmith)
        self.assertEqual(result, True)

        result = matcher.match(jsmith, jsmith_alt)
        self.assertEqual(result, False)

        result = matcher.match(jsmith_alt, jsmith)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jsmith_alt)
        self.assertEqual(False, result)

        result = matcher.match(jsmith_alt, john_smith)
        self.assertEqual(False, result)

        # Jane Rae matches Jane Rae Doe because they share
        # the same name "Jane Rae Doe"
        result = matcher.match(jrae, jrae_doe)
        self.assertEqual(result, True)

        result = matcher.match(jrae, jrae_doe)
        self.assertEqual(result, True)

        # No match with Jane Rae
        result = matcher.match(jsmith, jrae)
        self.assertEqual(result, False)

        result = matcher.match(jsmith, jrae_doe)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jrae)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jrae_doe)
        self.assertEqual(result, False)

        result = matcher.match(jsmith_alt, jrae)
        self.assertEqual(result, False)

        result = matcher.match(jsmith_alt, jrae_doe)
        self.assertEqual(result, False)

    def test_match_1(self):
        """Test match method"""

        # Let's define some identities first
        bstansberry = User(id=UUID('5b10f731-eee9-4a7d-95a5-e816d63bb1fa'), name=' Brian Stansberry', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True, identities=
        [Author(canonical_name=' Brian Stansberry <brian.stansberry@redhat.com>', aliases=None, name=' Brian Stansberry', email='brian.stansberry@redhat.com', user_id=UUID('5b10f731-eee9-4a7d-95a5-e816d63bb1fa')),
         Author(canonical_name='bstansberry@jboss.com <brian.stansberry@redhat.com>', aliases=None, name='bstansberry@jboss.com', email='brian.stansberry@redhat.com', user_id=UUID('5b10f731-eee9-4a7d-95a5-e816d63bb1fa')),
         Author(canonical_name='Brian Stansberry <brian.stansberry@redhat.com>', aliases=None, name='Brian Stansberry', email='brian.stansberry@redhat.com', user_id=UUID('5b10f731-eee9-4a7d-95a5-e816d63bb1fa'))])

        aogburn = User(id=UUID('0923b0a6-583f-4daf-9e20-c8fbced8cc84'), name='Aaron Ogburn', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True, identities=[Author(canonical_name='Aaron Ogburn <aogburn@redhat.com>', aliases=None, name='Aaron Ogburn', email='aogburn@redhat.com', user_id=UUID('0923b0a6-583f-4daf-9e20-c8fbced8cc84'))])

        abgopal = User(id=UUID('64b013cd-8772-4ce5-97da-fc2b0eba1220'), name='Abhilash Gopal', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True, identities=[Author(canonical_name='Abhilash Gopal <abgopal@microsoft.com>', aliases=None, name='Abhilash Gopal', email='abgopal@microsoft.com', user_id=UUID('64b013cd-8772-4ce5-97da-fc2b0eba1220'))])

        akovari = User(id=UUID('6bf87ace-ce20-4494-9649-6e183b60c3c2'), name='Adam Kovari', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True, identities=[Author(canonical_name='Adam Kovari <akovari@redhat.com>', aliases=None, name='Adam Kovari', email='akovari@redhat.com', user_id=UUID('6bf87ace-ce20-4494-9649-6e183b60c3c2'))])

        # Tests
        matcher = EmailNameMatcher()

        # First two unique identities must match
        result = matcher.match(bstansberry, aogburn)
        self.assertEqual(result, False)

        result = matcher.match(aogburn, bstansberry)
        self.assertEqual(result, False)

        # Comparing with the third only the first one
        # produces a match because of "John Smith" name
        result = matcher.match(bstansberry, abgopal)
        self.assertEqual(result, False)

        result = matcher.match(abgopal, bstansberry)
        self.assertEqual(result, False)

        result = matcher.match(aogburn, abgopal)
        self.assertEqual(False, result)

        result = matcher.match(abgopal, aogburn)
        self.assertEqual(False, result)

    def test_match_2(self):
        """Test match method"""

        # Let's define some identities first
        bstansberry = User(name='Jane Rae')
        bstansberry.identities = [Author(canonical_name='Jan Lanik <jlanik@redhat.com>', aliases=None, name='Jan Lanik', email='jlanik@redhat.com', user_id=UUID('d2e4d454-dd34-4963-81fb-c9f3eb1e6d9c'))]

        aogburn = User(name='Jane Rae')
        aogburn.identities = [Author(canonical_name='阿男 <l.weinan@gmail.com>', aliases=None, name='阿男', email='l.weinan@gmail.com', user_id=UUID('fe1b0a63-a7f0-452d-92f9-494e6400dc2d'))]

        jaikiran = User(name='Jane Rae')
        jaikiran.identities = [Author(canonical_name='Jaikiran <jaikiran.pai@gmail.com>', aliases=None, name='Jaikiran', email='jaikiran.pai@gmail.com', user_id=UUID('bf9d1e1b-b615-4816-8423-4d1a9ec4fc6b'))]


        # Tests
        matcher = EmailNameMatcher()

        # First two unique identities should bot match
        result = matcher.match(bstansberry, aogburn)
        self.assertEqual(result, False)

        result = matcher.match(aogburn, bstansberry)
        self.assertEqual(result, False)

        result = matcher.match(bstansberry, jaikiran)
        self.assertEqual(result, False)

        result = matcher.match(jaikiran, bstansberry)
        self.assertEqual(result, False)

    def test_no_match_same_email_username_unknown_name(self):
        """Test match method"""

        # Let's define some identities first
        bstansberry = User(id=UUID('6b5ecbdc-3fc9-4b09-a5b8-53a0d7b4dff7'), name='Donnic', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True,
                           identities=[Author(canonical_name='Donnic <v-ledou@microsoft.com>', aliases=None, name='Donnic', email='v-ledou@microsoft.com', user_id=UUID('6b5ecbdc-3fc9-4b09-a5b8-53a0d7b4dff7')),
                                       Author(canonical_name='v-ledou <v-ledou@microsoft.com>', aliases=None, name='v-ledou', email='v-ledou@microsoft.com', user_id=UUID('6b5ecbdc-3fc9-4b09-a5b8-53a0d7b4dff7'))])

        aogburn = User(id=UUID('445d5876-acfc-44ee-a1b4-2380968416cb'), name='unknown', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True,
                       identities=[Author(canonical_name='unknown <v-ledou@xianwin81-v02.fareast.corp.microsoft.com>', aliases=None, name='unknown', email='v-ledou@xianwin81-v02.fareast.corp.microsoft.com', user_id=UUID('445d5876-acfc-44ee-a1b4-2380968416cb'))])

        jaikiran = User(id=UUID('45f0578c-9f61-4f11-bf14-61c72b4870b1'), name='unknown', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True,
                        identities=[Author(canonical_name='unknown <v-ledou@xianwin81-v01.fareast.corp.microsoft.com>', aliases=None, name='unknown', email='v-ledou@xianwin81-v01.fareast.corp.microsoft.com', user_id=UUID('45f0578c-9f61-4f11-bf14-61c72b4870b1'))])


        # Tests
        matcher = EmailNameMatcher()

        # First two unique identities should bot match
        result = matcher.match(bstansberry, aogburn)
        self.assertEqual(result, False)

        result = matcher.match(aogburn, bstansberry)
        self.assertEqual(result, False)

        result = matcher.match(bstansberry, jaikiran)
        self.assertEqual(result, False)

        result = matcher.match(jaikiran, bstansberry)
        self.assertEqual(result, False)

        result = matcher.match(jaikiran, aogburn)
        self.assertEqual(result, False)

    def test_no_match_same_email_username_empty_name(self):
        """Test match method"""

        # Let's define some identities first
        bstansberry = User(id=UUID('6b5ecbdc-3fc9-4b09-a5b8-53a0d7b4dff7'), name='Donnic', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True,
                           identities=[Author(canonical_name='Donnic <v-ledou@microsoft.com>', aliases=None, name='Donnic', email='v-ledou@microsoft.com', user_id=UUID('6b5ecbdc-3fc9-4b09-a5b8-53a0d7b4dff7')),
                                       Author(canonical_name='v-ledou <v-ledou@microsoft.com>', aliases=None, name='v-ledou', email='v-ledou@microsoft.com', user_id=UUID('6b5ecbdc-3fc9-4b09-a5b8-53a0d7b4dff7'))])

        aogburn = User(id=UUID('445d5876-acfc-44ee-a1b4-2380968416cb'), name='unknown', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True,
                       identities=[Author(canonical_name='unknown <v-ledou@xianwin81-v02.fareast.corp.microsoft.com>', aliases=None, name='', email='v-ledou@xianwin81-v02.fareast.corp.microsoft.com', user_id=UUID('445d5876-acfc-44ee-a1b4-2380968416cb'))])

        jaikiran = User(id=UUID('45f0578c-9f61-4f11-bf14-61c72b4870b1'), name='unknown', primary_email=None, is_active=True, description=None, workplace=None, location=None, website=None, twitter=None, is_show_email=True,
                        identities=[Author(canonical_name='unknown <v-ledou@xianwin81-v01.fareast.corp.microsoft.com>', aliases=None, name='', email='v-ledou@xianwin81-v01.fareast.corp.microsoft.com', user_id=UUID('45f0578c-9f61-4f11-bf14-61c72b4870b1'))])


        # Tests
        matcher = EmailNameMatcher()

        # First two unique identities should bot match
        result = matcher.match(bstansberry, aogburn)
        self.assertEqual(False, result)

        result = matcher.match(aogburn, bstansberry)
        self.assertEqual(False, result)

        result = matcher.match(bstansberry, jaikiran)
        self.assertEqual(False, result)

        result = matcher.match(jaikiran, bstansberry)
        self.assertEqual(False, result,)

        result = matcher.match(jaikiran, aogburn)
        self.assertEqual(False, result)

    def test_match_Fitzgerald(self):
        """Test match method"""

        # Let's define some identities first
        garious = User(name='Greg Fitzgerald')
        garious.identities = [Author(canonical_name='Greg Fitzgerald <garious@gmail.com>', aliases=None, name='Greg Fitzgerald', email='garious@gmail.com', user_id=UUID('a3cc20c4-2134-417b-80e8-c003df2a0631'))]

        greg = User(name='Greg Fitzgerald')
        greg.identities = [Author(canonical_name='Greg Fitzgerald <greg@solana.com>', aliases=None, name='Greg Fitzgerald', email='greg@solana.com', user_id=UUID('a3cc20c4-2134-417b-80e8-c003df2a0631'))]

        burnto = User(name='Brent Fitzgerald')
        burnto.identities = [Author(canonical_name='Brent Fitzgerald <burnto@gmail.com>', aliases=None, name='Brent Fitzgerald', email='burnto@gmail.com', user_id=None)]


        # Tests
        matcher = EmailNameMatcher()

        # First two unique identities should match
        result = matcher.match(garious, greg)
        self.assertEqual(result, True)

        result = matcher.match(greg, garious)
        self.assertEqual(result, True)

        # Third identity should not macth the first two identities
        result = matcher.match(greg, burnto)
        self.assertEqual(result, False)

        result = matcher.match(burnto, greg)
        self.assertEqual(result, False)

        result = matcher.match(garious, burnto)
        self.assertEqual(result, False)

        result = matcher.match(burnto, garious)
        self.assertEqual(result, False)

    def test_match_michael(self):
        """Test match method"""

        # Let's define some identities first
        Michael_Bannister = User(name='Michael Bannister')
        Michael_Bannister.identities = [
            Author(canonical_name='Michael Bannister <github@michaelbannister.co.uk>', aliases=None,
                   name='Michael Bannister', email='github@michaelbannister.co.uk', user_id=Michael_Bannister.id)]

        michael = User(name='michael')
        michael.identities = [
            Author(canonical_name='michael <michael@localhost.localdomain>', aliases=None, name='michael',
                   email='michael@localhost.localdomain', user_id=michael.id)]

        Michael_Wermeester = User(name='Michael Wermeester')
        Michael_Wermeester.identities = [
            Author(canonical_name='Michael Wermeester <michael.wermeester@me.com>', aliases=None,
                   name='Michael Wermeester', email='michael.wermeester@me.com', user_id=Michael_Wermeester.id)]

        Michael_Pellegrini = User(name='Michael Pellegrini')
        Michael_Pellegrini.identities = [
            Author(canonical_name='Michael Pellegrini <mike.pellegrini@allegiantair.com>', aliases=None,
                   name='Michael Pellegrini', email='mike.pellegrini@allegiantair.com', user_id=Michael_Pellegrini.id)]

        Michael_Musgrove = User(name='Michael Musgrove')
        Michael_Musgrove.identities = [
            Author(canonical_name='Michael Musgrove <mmusgrov@redhat.com>', aliases=None, name='Michael Musgrove',
                   email='mmusgrov@redhat.com', user_id=Michael_Musgrove.id)]

        mmusgrov = User(name='mmusgrov')
        mmusgrov.identities = [Author(canonical_name='mmusgrov <mmusgrov@redhat.com>', aliases=None, name='mmusgrov',
                                      email='mmusgrov@redhat.com', user_id=mmusgrov.id)]

        Michael_Levin = User(name='Michael Levin')
        Michael_Levin.identities = [
            Author(canonical_name='Michael Levin <kinnetica@gmail.com>', aliases=None, name='Michael Levin',
                   email='kinnetica@gmail.com', user_id=Michael_Levin.id)]

        Michael_Edgar = User(name='Michael Edgar')
        Michael_Edgar.identities = [
            Author(canonical_name='Michael Edgar <michael@xlate.io>', aliases=None, name='Michael Edgar',
                   email='michael@xlate.io', user_id=Michael_Edgar.id)]

        # Tests
        matcher = EmailNameMatcher()

        # First two unique identities should bot match
        result = matcher.match(Michael_Bannister, michael)
        self.assertEqual(result, False)

        result = matcher.match(michael, Michael_Bannister)
        self.assertEqual(result, False)

        result = matcher.match(Michael_Bannister, Michael_Wermeester)
        self.assertEqual(result, False)

        result = matcher.match(Michael_Wermeester, Michael_Bannister)
        self.assertEqual(result, False)

        result = matcher.match(Michael_Levin, Michael_Edgar)
        self.assertEqual(result, False)

        result = matcher.match(Michael_Edgar, Michael_Levin)
        self.assertEqual(result, False)


    def test_match_with_blacklist(self):
        """Test match when there are entries in the blacklist"""

        jsmith = User(name='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@example.com>', name='John Smith', email='jsmith@example.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        john_smith = User(name='js')
        john_smith.identities = [Author(canonical_name='John Smith JR <>', name='John Smith JR', email='', user_id=john_smith.id),
                                 Author(canonical_name=' <>', name='', email='', user_id=john_smith.id),
                                 Author(canonical_name='Smith. J <>', name='Smith. J', email='', user_id=john_smith.id),
                                 Author(canonical_name='Smith. J <JSmith@example.com>', name='Smith. J', email='JSmith@example.com', user_id=john_smith.id)]

        jsmith_alt = User(name='J. Smith')
        jsmith_alt.identities = [Author(canonical_name='John Smith JR <>', name='John Smith JR', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <>', name='', email='', user_id=jsmith_alt.id),
                                 Author(canonical_name=' <jsmith>', name='', email='jsmith', user_id=jsmith_alt.id)]

        # Tests
        bl = [MatchingBlacklist(excluded='John Smith'),
              MatchingBlacklist(excluded='jsmith@example.com')]

        matcher = EmailNameMatcher(blacklist=bl)

        result = matcher.match(jsmith, john_smith)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jsmith)
        self.assertEqual(result, False)

        # John Smith is blacklisted, so no match
        result = matcher.match(jsmith, jsmith_alt)
        self.assertEqual(result, False)

        result = matcher.match(jsmith_alt, jsmith)
        self.assertEqual(result, False)

        result = matcher.match(john_smith, jsmith_alt)
        self.assertEqual(result, False)

        result = matcher.match(jsmith_alt, john_smith)
        self.assertEqual(result, False)

    def test_match_same_identity(self):
        """Test whether there is a match comparing the same identity"""

        uid = User(name='John Smith')

        matcher = EmailNameMatcher()
        result = matcher.match(uid, uid)

        self.assertEqual(result, True)

    def test_match_same_uuid(self):
        """Test if there is a match when compares identities with the same UUID"""

        uid1 = User(id='d8bb2470-595f-4cef-9d3c-b2b016dd7625')
        uid2 = User(id='d8bb2470-595f-4cef-9d3c-b2b016dd7625')

        matcher = EmailNameMatcher()

        result = matcher.match(uid1, uid2)
        self.assertEqual(result, True)

        result = matcher.match(uid2, uid1)
        self.assertEqual(result, True)

        # None UUIDs do not produce a positive match
        uid1 = User(id=None)
        uid2 = User(id=None)

        matcher = EmailNameMatcher()

        result = matcher.match(uid1, uid2)
        self.assertEqual(result, False)

        result = matcher.match(uid2, uid1)
        self.assertEqual(result, False)

    def test_match_identities_instances(self):
        """Test whether it raises an error when ids are not UniqueIdentities"""

        uid = User(name='John Smith')

        matcher = EmailNameMatcher()

        self.assertRaises(ValueError, matcher.match, 'John Smith', uid)
        self.assertRaises(ValueError, matcher.match, uid, 'John Smith')
        self.assertRaises(ValueError, matcher.match, None, uid)
        self.assertRaises(ValueError, matcher.match, uid, None)
        self.assertRaises(ValueError, matcher.match, 'John Smith', 'John Doe')

    def test_filter_identities_with_blacklist(self):
        """Test if identities are filtered when there is a blacklist"""

        # Let's define some identities first
        jsmith = User(name='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name='John Smith JR <>', name='John Smith JR', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        jrae = User(uuid='jrae')
        jrae.identities = [Author(canonical_name='Jane Rae <>', name='Jane Rae', email='', user_id=jrae.id),
                           Author(canonical_name='Jane Rae Doe <jane.rae@example.net>', name='Jane Rae Doe', email='jane.rae@example.net', user_id=jrae.id),
                           Author(canonical_name='jrae <>', name='jrae', email='', user_id=jrae.id),
                           Author(canonical_name=' <JRAE@example.net>', name='', email='JRAE@example.net', user_id=jrae.id)]

        # Tests
        bl = [MatchingBlacklist(excluded='John Smith'),
              MatchingBlacklist(excluded='jrae@example.net')]

        matcher = EmailNameMatcher(blacklist=bl)

        result = matcher.filter(jsmith)
        self.assertEqual(1, len(result),)

        fid = result[0]
        self.assertIsInstance(fid, Author)
        self.assertEqual(fid.user_id, jsmith.id)
        self.assertEqual(fid.name, 'John Smith JR')
        self.assertEqual('jsmith@google.com',fid.email)

        result = matcher.filter(jrae)
        self.assertEqual(1, len(result))

        fid = result[0]
        self.assertIsInstance(fid, Author)
        self.assertEqual(fid.user_id, jrae.id)
        self.assertEqual(fid.name, 'Jane Rae Doe')
        self.assertEqual(fid.email, 'jane.rae@example.net')

    def test_filter_identities_instances(self):
        """Test whether it raises an error when id is not a User"""

        matcher = EmailNameMatcher()

        self.assertRaises(ValueError, matcher.filter, 'John Smith')
        self.assertRaises(ValueError, matcher.filter, None)

    def test_matching_criteria(self):
        """Test whether it returns the matching criteria keys"""

        criteria = EmailNameMatcher.matching_criteria()

        self.assertListEqual(criteria, ['email', 'name'])

    def test_filter_identities_with_domains_blacklist(self):
        """Test if identities are filtered when there is a blacklist"""

        # Let's define some identities first
        jsmith = User(name='jsmith')
        jsmith.identities = [Author(canonical_name='John Smith <jsmith@google.com>', name='John Smith', email='jsmith@google.com', user_id=jsmith.id),
                             Author(canonical_name='John Smith <>', name='John Smith', email='', user_id=jsmith.id),
                             Author(canonical_name='John Smith JR <>', name='John Smith JR', email='jsmith@travis-ci.org', user_id=jsmith.id),
                             Author(canonical_name=' <>', name='', email='', user_id=jsmith.id)]

        # Tests
        matcher = EmailNameMatcher()

        result = matcher.filter(jsmith)
        self.assertEqual(1, len(result),)

        fid = result[0]
        self.assertIsInstance(fid, Author)
        self.assertEqual(fid.user_id, jsmith.id)
        self.assertEqual('John Smith', fid.name)
        self.assertEqual('jsmith@google.com',fid.email)


if __name__ == "__main__":
    unittest.main()
