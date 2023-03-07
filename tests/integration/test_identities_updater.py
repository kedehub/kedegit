import unittest
import datetime
import os
from uuid import UUID

from tests.kedegit_test import KedeGitTest
from kedehub.services.identities_updater import identity_merge_users, create_users_dict, merge_users, \
    identify_authors_to_merge, save_identified_merged_users, auto_confirmation, \
    identify_authors_to_merge_with_human_help
from kedehub.utility.input_utility import get_bool_input
from kedehub.services.dro.author_dto import Author
from kedehub.services.dro.user_dto import User
from kedehub.services.author_service import save_new_author
from kedehub.services.user_service import create_new_user


class IdentitiesUpdaterTestCases(KedeGitTest):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def _populate_db(self):

        self.cloned_worktree = os.path.join(self.working_directory.name, 'worktree')
        self.start_date = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos'),
                                    os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json'),
                                    earliest_date=self.start_date)


    def test_identities_updater_all_new_users_each_with_one_author(self):

        self._populate_db()

        len_users, len_authors, len_matched_users_by_email, len_matched_users_by_email_and_name, \
        authors_updated, users_inserted, users_merged_count, authors_merged_count = identity_merge_users(['test'])

        self.assertEqual(4, len_users)
        self.assertEqual(5, len_authors)
        self.assertEqual(4, len_matched_users_by_email)
        self.assertEqual(4, len_matched_users_by_email_and_name)
        self.assertEqual(0, users_merged_count)
        self.assertEqual(0, authors_merged_count)
        self.assertEqual(0, authors_updated)
        self.assertEqual(4, users_inserted)
        self.assertEqual(authors_merged_count, authors_updated)

    def test_identities_updater_all_new_users_each_with_one_author_repeated(self):

        self._populate_db()

        len_users, len_authors, len_matched_users_by_email, len_matched_users_by_email_and_name, \
        authors_updated, users_inserted, users_merged_count, authors_merged_count = identity_merge_users(['test'])

        self.assertEqual(4, len_users)
        self.assertEqual(5, len_authors)
        self.assertEqual(4, len_matched_users_by_email)
        self.assertEqual(4, len_matched_users_by_email_and_name)
        self.assertEqual(0, users_merged_count)
        self.assertEqual(0, authors_merged_count)
        self.assertEqual(0, authors_updated)
        self.assertEqual(4, users_inserted)
        self.assertEqual(authors_merged_count, authors_updated)

        len_users, len_authors, len_matched_users_by_email, len_matched_users_by_email_and_name, \
        authors_updated, users_inserted, users_merged_count, authors_merged_count = identity_merge_users(['test'])

        self.assertEqual(4, len_users)
        self.assertEqual(5, len_authors)
        self.assertEqual(4, len_matched_users_by_email)
        self.assertEqual(4, len_matched_users_by_email_and_name)
        self.assertEqual(0, users_merged_count)
        self.assertEqual(0, authors_merged_count)
        self.assertEqual(0, authors_updated)
        self.assertEqual(0, users_inserted)
        self.assertEqual(authors_merged_count, authors_updated)

    def test_identities_updater(self):

        authors = {
            'Pragna Gopa <pgopa@microsoft.com>': Author(canonical_name='Pragna Gopa <pgopa@microsoft.com>',
                                                        aliases=None, name='Pragna Gopa', email='pgopa@microsoft.com',
                                                        user_id=None),
            'Pragna Gopa <pragna.gopa@hotmail.com>': Author(canonical_name='Pragna Gopa <pragna.gopa@hotmail.com>',
                                                            aliases=None, name='Pragna Gopa',
                                                            email='pragna.gopa@hotmail.com', user_id=None),
            'Abhishek Kumar <abhiku@microsoft.com>': Author(canonical_name='Abhishek Kumar <abhiku@microsoft.com>',
                                                            aliases=None, name='Abhishek Kumar',
                                                            email='abhiku@microsoft.com', user_id=None),
            'Adrian Hall <adrian@shellmonger.com>': Author(canonical_name='Adrian Hall <adrian@shellmonger.com>',
                                                           aliases=None, name='Adrian Hall',
                                                           email='adrian@shellmonger.com', user_id=None),
            'Alexey Rodionov <alrod@microsoft.com>': Author(canonical_name='Alexey Rodionov <alrod@microsoft.com>',
                                                            aliases=None, name='Alexey Rodionov',
                                                            email='alrod@microsoft.com',
                                                            user_id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1')),
            'Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>': Author(
                canonical_name='Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>', aliases=None, name='Donna Malayeri',
                email='DonnaM@Donnas-MacBook-Air.local', user_id=None),
            'Donna Malayeri <DonnaM@erik_winters.northamerica.corp.microsoft.com>': Author(
                canonical_name='Donna Malayeri <DonnaM@erik_winters.northamerica.corp.microsoft.com>', aliases=None,
                name='Donna Malayeri', email='DonnaM@erik_winters.northamerica.corp.microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
            'Donna Malayeri <DonnaM@jimwan-carbon.northamerica.corp.microsoft.com>': Author(
                canonical_name='Donna Malayeri <DonnaM@jimwan-carbon.northamerica.corp.microsoft.com>', aliases=None,
                name='Donna Malayeri', email='DonnaM@jimwan-carbon.northamerica.corp.microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
            'Donna Malayeri <DonnaM@mattshel-asus.redmond.corp.microsoft.com>': Author(
                canonical_name='Donna Malayeri <DonnaM@mattshel-asus.redmond.corp.microsoft.com>', aliases=None,
                name='Donna Malayeri', email='DonnaM@mattshel-asus.redmond.corp.microsoft.com', user_id=None),
            'Donna Malayeri <donnam@microsoft.com>': Author(canonical_name='Donna Malayeri <donnam@microsoft.com>',
                                                            aliases=None, name='Donna Malayeri',
                                                            email='donnam@microsoft.com', user_id=None)}

        for author in authors.values():
            try:
                save_new_author(author.canonical_name)
            except Exception as e:
                print('Author: {}'.format(e))

        len_matched_users_by_email, len_matched_users_by_email_and_name, len_users, len_authors, matched_users_by_email_and_name, users_merged_count, authors_merged_count = identify_authors_to_merge(
            authors)

        authors_updated, users_inserted = save_identified_merged_users(matched_users_by_email_and_name)

        self.assertEqual(8, len_users)
        self.assertEqual(10, len_authors)
        self.assertEqual(8, len_matched_users_by_email)
        self.assertEqual(5, len_matched_users_by_email_and_name)
        self.assertEqual(3, users_merged_count)
        self.assertEqual(3, authors_merged_count)
        self.assertEqual(3, users_inserted)
        self.assertEqual(3, authors_updated)
        self.assertEqual(authors_merged_count, authors_updated)

    def test_identities_updater_confidence_07(self):

        authors = {
            'Alexandre Kurth <alexandre.kurth@gmail.com>': Author(
                canonical_name='Alexandre Kurth <alexandre.kurth@gmail.com>',
                aliases=None, name='Alexandre Kurth', email='alexandre.kurth@gmail.com',
                user_id=UUID('161da6f4-9699-46b3-9330-c0016b3bc148')),
            'Alex Prut <1648497+alexprut@users.noreply.github.com>': Author(
                canonical_name='Alex Prut <1648497+alexprut@users.noreply.github.com>',
                aliases=None, name='Alex Prut', email='1648497+alexprut@users.noreply.github.com',
                user_id=UUID('161da6f4-9699-46b3-9330-c0016b3bc145')),
            'Alex Prut <alexandru@blockchain.com>': Author(canonical_name='Alex Prut <alexandru@blockchain.com>',
                                                           aliases=None, name='Alex Prut',
                                                           email='alexandru@blockchain.com',
                                                           user_id=UUID('161da6f4-9699-46b3-9330-c0016b3bc145'))}

        for author in authors.values():
            try:
                save_new_author(author.canonical_name)
            except Exception as e:
                print('Author: {}'.format(e))

        len_matched_users_by_email, len_matched_users_by_email_and_name, len_users, len_authors, matched_users_by_email_and_name, users_merged_count, \
        authors_merged_count = identify_authors_to_merge_with_human_help(authors, confidence_level=0.7)

        authors_updated, users_inserted = save_identified_merged_users(matched_users_by_email_and_name)

        self.assertEqual(2, len_users)
        self.assertEqual(3, len_authors)
        self.assertEqual(1, len_matched_users_by_email_and_name)
        self.assertEqual(0, users_merged_count)
        self.assertEqual(0, authors_merged_count)
        self.assertEqual(0, users_inserted)
        self.assertEqual(0, authors_updated)
        self.assertEqual(authors_merged_count, authors_updated)

    def test_identities_updater_confidence_099(self):

        authors = {
            'Alexandre Kurth <alexandre.kurth@gmail.com>': Author(canonical_name='Alexandre Kurth <alexandre.kurth@gmail.com>',
                                                                  aliases=None, name='Alexandre Kurth', email='alexandre.kurth@gmail.com',
                                                                  user_id=UUID('161da6f4-9699-46b3-9330-c0016b3bc148')),
            'Alex Prut <1648497+alexprut@users.noreply.github.com>': Author(canonical_name='Alex Prut <1648497+alexprut@users.noreply.github.com>',
                                                                            aliases=None, name='Alex Prut', email='1648497+alexprut@users.noreply.github.com',
                                                                            user_id=UUID('161da6f4-9699-46b3-9330-c0016b3bc145')),
            'Alex Prut <alexandru@blockchain.com>': Author(canonical_name='Alex Prut <alexandru@blockchain.com>',
                                                           aliases=None, name='Alex Prut', email='alexandru@blockchain.com',
                                                           user_id=UUID('161da6f4-9699-46b3-9330-c0016b3bc145'))}

        for author in authors.values():
            try:
                save_new_author(author.canonical_name)
            except Exception as e:
                print('Author: {}'.format(e))

        len_matched_users_by_email, len_matched_users_by_email_and_name, len_users, len_authors, matched_users_by_email_and_name, users_merged_count, \
        authors_merged_count = identify_authors_to_merge_with_human_help(authors, confidence_level = 0.99)

        authors_updated, users_inserted = save_identified_merged_users(matched_users_by_email_and_name)

        self.assertEqual(2, len_users)
        self.assertEqual(3, len_authors)
        self.assertEqual(2, len_matched_users_by_email_and_name)
        self.assertEqual(0, users_merged_count)
        self.assertEqual(0, authors_merged_count)
        self.assertEqual(0, users_inserted)
        self.assertEqual(0, authors_updated)
        self.assertEqual(authors_merged_count, authors_updated)


    def test_identities_updater_add_authors_to_existing_user(self):

        authors = {
            'Ryan M. Shea <8948187+rmshea@users.noreply.github.com>':
                Author(canonical_name='Ryan M. Shea <8948187+rmshea@users.noreply.github.com>', aliases=None,
                        name='Ryan M. Shea', email='8948187+rmshea@users.noreply.github.com', user_id=None),
            'Ryan Shea <ryan@solana.com>':
                Author(canonical_name='Ryan Shea <ryan@solana.com>', aliases=None,
                       name='Ryan Shea', email='ryan@solana.com', user_id=None),
            'R. M. Shea <8948187+rmshea@users.noreply.github.com>':
                Author(canonical_name='R. M. Shea <8948187+rmshea@users.noreply.github.com>', aliases=None,
                        name='R. M. Shea', email='8948187+rmshea@users.noreply.github.com', user_id=None),
            'Ryan Shea <rmshea@users.noreply.github.com>':
                Author(canonical_name='Ryan Shea <rmshea@users.noreply.github.com>', aliases=None,
                        name='Ryan Shea', email='rmshea@users.noreply.github.com', user_id=None),
            'Ryan Shea <ryan-shea@users.noreply.github.com>':
                Author(canonical_name='Ryan Shea <ryan-shea@users.noreply.github.com>', aliases=None,
                        name='Ryan Shea', email='ryan-shea@users.noreply.github.com', user_id=None),
            'rmshea <8948187+rmshea@users.noreply.github.com>':
                Author(canonical_name='rmshea <8948187+rmshea@users.noreply.github.com>', aliases=None,
                       name='rmshea', email='8948187+rmshea@users.noreply.github.com', user_id=None)
            }

        for author in authors.values():
            try:
                save_new_author(author.canonical_name)
            except Exception as e:
                print('Author: {}'.format(e))

        # remove the last authors
        last_author = authors.popitem()
        # create user for one of the authors
        user = User(name=last_author[1].name,
                       primary_email=last_author[1].email,
                       is_active=True)
        create_new_user(user)

        len_matched_users_by_email, len_matched_users_by_email_and_name, len_users, len_authors, matched_users_by_email_and_name, users_merged_count, authors_merged_count = identify_authors_to_merge(
            authors)

        authors_updated, users_inserted = save_identified_merged_users(matched_users_by_email_and_name)

        self.assertEqual(5, len_users)
        self.assertEqual(5, len_authors)
        self.assertEqual(4, len_matched_users_by_email)
        self.assertEqual(1, len_matched_users_by_email_and_name)
        self.assertEqual(4, users_merged_count)
        self.assertEqual(4, authors_merged_count)
        self.assertEqual(0, users_inserted)
        self.assertEqual(4, authors_updated)
        self.assertEqual(authors_merged_count, authors_updated)

    def test_create_users_dict(self):
        authors = {
            'Pragna Gopa <pgopa@microsoft.com>': Author(canonical_name='Pragna Gopa <pgopa@microsoft.com>',
                                                        aliases=None, name='Pragna Gopa', email='pgopa@microsoft.com',
                                                        user_id=None),
            'Pragna Gopa <pragna.gopa@hotmail.com>': Author(canonical_name='Pragna Gopa <pragna.gopa@hotmail.com>',
                                                            aliases=None, name='Pragna Gopa',
                                                            email='pragna.gopa@hotmail.com', user_id=None),
            'Abhishek Kumar <abhiku@microsoft.com>': Author(canonical_name='Abhishek Kumar <abhiku@microsoft.com>',
                                                            aliases=None, name='Abhishek Kumar',
                                                            email='abhiku@microsoft.com', user_id=None),
            'Adrian Hall <adrian@shellmonger.com>': Author(canonical_name='Adrian Hall <adrian@shellmonger.com>',
                                                           aliases=None, name='Adrian Hall',
                                                           email='adrian@shellmonger.com', user_id=None),
            'Alexey Rodionov <alrod@microsoft.com>': Author(canonical_name='Alexey Rodionov <alrod@microsoft.com>',
                                                            aliases=None, name='Alexey Rodionov',
                                                            email='alrod@microsoft.com',
                                                            user_id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1')),
            'Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>': Author(
                canonical_name='Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>', aliases=None, name='Donna Malayeri',
                email='DonnaM@Donnas-MacBook-Air.local', user_id=None),
            'Donna Malayeri <DonnaM@erik_winters.northamerica.corp.microsoft.com>': Author(
                canonical_name='Donna Malayeri <DonnaM@erik_winters.northamerica.corp.microsoft.com>', aliases=None,
                name='Donna Malayeri', email='DonnaM@erik_winters.northamerica.corp.microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
            'Donna Malayeri <DonnaM@jimwan-carbon.northamerica.corp.microsoft.com>': Author(
                canonical_name='Donna Malayeri <DonnaM@jimwan-carbon.northamerica.corp.microsoft.com>', aliases=None,
                name='Donna Malayeri', email='DonnaM@jimwan-carbon.northamerica.corp.microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
            'Donna Malayeri <DonnaM@mattshel-asus.redmond.corp.microsoft.com>': Author(
                canonical_name='Donna Malayeri <DonnaM@mattshel-asus.redmond.corp.microsoft.com>', aliases=None,
                name='Donna Malayeri', email='DonnaM@mattshel-asus.redmond.corp.microsoft.com', user_id=None),
            'Donna Malayeri <donnam@microsoft.com>': Author(canonical_name='Donna Malayeri <donnam@microsoft.com>',
                                                            aliases=None, name='Donna Malayeri',
                                                            email='donnam@microsoft.com', user_id=None)}

        users = create_users_dict(authors)

        # check that 10 authors ar assigned to 9 users
        self.assertEqual(8, len(users))

        # check if the authors who had user_id=None now have UUID and is_actibe=False
        for id in users:
            current_user = users[id]
            current_author = authors[current_user.identities[0].canonical_name]
            if current_author.canonical_name in ['Pragna Gopa <pgopa@microsoft.com>', 'Pragna Gopa <pragna.gopa@hotmail.com>',
                                                 'Abhishek Kumar <abhiku@microsoft.com>', 'Adrian Hall <adrian@shellmonger.com>',
                                                 'Donna Malayeri <DonnaM@mattshel-asus.redmond.corp.microsoft.com>',
                                                 'Donna Malayeri <donnam@microsoft.com>']:
                self.assertEqual(False,current_user.is_active)
                self.assertIsNotNone(current_author.user_id)

        # check that removed is 'Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>'
        for id in users:
            current_user = users[id]
            current_author = authors[current_user.identities[0].canonical_name]

            self.assertNotIn(current_author.canonical_name, ['Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>'])

        # check if two authors with the same existing user_id are assigned to the same user is_active=True
        self.assertEqual(User(id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c'),
                                                               name='Donna Malayeri', primary_email='DonnaM@jimwan-carbon.northamerica.corp.microsoft.com',
                                                               is_active=True, description=None, workplace=None,
                                                               location=None, website=None, twitter=None,
                                                               is_show_email=True, identities=[
                    Author(canonical_name='Donna Malayeri <DonnaM@erik_winters.northamerica.corp.microsoft.com>',
                           aliases=None, name='Donna Malayeri',
                           email='DonnaM@erik_winters.northamerica.corp.microsoft.com',
                           user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
                    Author(canonical_name='Donna Malayeri <DonnaM@jimwan-carbon.northamerica.corp.microsoft.com>',
                           aliases=None, name='Donna Malayeri',
                           email='DonnaM@jimwan-carbon.northamerica.corp.microsoft.com',
                           user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c'))]),
                         users[UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')])

        # check if an author with an existing user_id is assigned to a user with the same id is_active=True
        self.assertEqual(User(id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1'),
                                                               name='Alexey Rodionov', primary_email='alrod@microsoft.com',
                                                               is_active=True, description=None, workplace=None,
                                                               location=None, website=None, twitter=None,
                                                               is_show_email=True, identities=[
                    Author(canonical_name='Alexey Rodionov <alrod@microsoft.com>', aliases=None, name='Alexey Rodionov',
                           email='alrod@microsoft.com', user_id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1'))]),users[UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1')])

    def test_create_users_dict_users_noreply_github_com(self):
        authors = {
            'Pragna Gopa <pgopa@users.noreply.github.com>': Author(canonical_name='Pragna Gopa <pgopa@users.noreply.github.com>',
                                                        aliases=None, name='Pragna Gopa', email='pgopa@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        # check that 10 authors ar assigned to 9 users
        self.assertEqual(1, len(users))

        # check if the authors who had user_id=None now have UUID and is_actibe=False
        for id in users:
            current_user = users[id]
            current_author = authors[current_user.identities[0].canonical_name]

            self.assertEqual(False,current_user.is_active)
            self.assertIsNotNone(current_author.user_id)

    def test_create_users_dict_bot_users_noreply_github_com(self):
        '''
        If the author email is not valit then user primary_email must be autogenerated for @users.noreply.kedegub.io
        '''
        authors = {
            'Pragna Gopa <pgopa[bot]@users.noreply.github.com>': Author(canonical_name='Pragna Gopa <pgopa[bot]@users.noreply.github.com>',
                                                        aliases=None, name='Pragna Gopa', email='pgopa[bot]@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        # check that 10 authors ar assigned to 9 users
        self.assertEqual(1, len(users))

        # check if the authors who had user_id=None now have UUID and is_actibe=False
        for id in users:
            current_user = users[id]
            current_author = authors[current_user.identities[0].canonical_name]

            self.assertEqual(False,current_user.is_active)
            self.assertIsNotNone(current_author.user_id)
            self.assertEqual(str(current_user.id) + '@users.noreply.kedegub.io', current_user.primary_email)

    def test_create_users_dict_dependabot_bot_pre_2017_github_email(self):
        '''
        Bot detection by name
        '''
        authors = {
            'dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>': Author(canonical_name='dependabot[bot] <dependabot[bot]@users.noreply.github.com>',
                                                        aliases=None, name='dependabot[bot]', email='dependabot[bot]@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        self.assertEqual(0, len(users))

    def test_create_users_dict_dependabot_bot_post_2017_github_email(self):
        '''
        Bot detection by name
        '''
        authors = {
            'dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>': Author(canonical_name='dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>',
                                                        aliases=None, name='dependabot[bot]', email='49699333+dependabot[bot]@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        self.assertEqual(0, len(users))

    def test_create_users_dict_dependabot_bot_buildkite(self):
        '''
        Bot detection by name
        '''
        authors = {
            'dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>': Author(canonical_name='dependabot-buildkite <dependabot-buildkite@users.noreply.github.com>',
                                                        aliases=None, name='dependabot-buildkite', email='dependabot-buildkite@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        self.assertEqual(0, len(users))

    def test_create_users_dict_dependabot_preview_bot_buildkite(self):
        '''
        Bot detection by name
        '''
        authors = {
            'dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>': Author(canonical_name='dependabot-preview[bot] <dependabot-preview[bot]@users.noreply.github.com>',
                                                        aliases=None, name='dependabot-preview[bot]', email='dependabot-preview[bot]@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        self.assertEqual(0, len(users))

    def test_create_users_dict_mergify_bot(self):
        '''
        Bot detection by name
        '''
        authors = {
            'mergify[bot] <49699333+mergify[bot]@users.noreply.github.com>': Author(canonical_name='mergify[bot] <mergify[bot]@users.noreply.github.com>',
                                                        aliases=None, name='mergify[bot]', email='mergify[bot]@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        self.assertEqual(0, len(users))

    def test_create_users_dict_mergify(self):
        '''
        Bot detection by name
        '''
        authors = {
            'mergify-bot <noreply@mergify.io>': Author(canonical_name='mergify-bot <noreply@mergify.io>',
                                                        aliases=None, name='mergify-bot', email='noreply@mergify.io',
                                                        user_id=None)}

        users = create_users_dict(authors)

        self.assertEqual(0, len(users))

    def test_create_users_dict_github_actions_bot(self):
        '''
        Bot detection by name
        '''
        authors = {
            'github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>': Author(canonical_name='github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>',
                                                        aliases=None, name='github-actions[bot]', email='41898282+github-actions[bot]@users.noreply.github.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        self.assertEqual(0, len(users))

    def test_create_users_dict_Anonymous(self):
        '''
        If the author email is not valit then user primary_email must be autogenerated for @users.noreply.kedegub.io
        '''
        authors = {
            'Anonymous <anonymous@overleaf.com>': Author(canonical_name='Anonymous <anonymous@overleaf.com>',
                                                        aliases=None, name='Anonymous', email='anonymous@overleaf.com',
                                                        user_id=None)}

        users = create_users_dict(authors)

        # check that 10 authors ar assigned to 9 users
        self.assertEqual(0, len(users))

    def test_merge_users(self):

        users = [
                [User(id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'), name='Pragna Gopa', primary_email=None,
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                        Author(canonical_name='Pragna Gopa <pgopa@microsoft.com>', aliases=None, name='Pragna Gopa',
                       email='pgopa@microsoft.com', user_id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'))]),
                User(id=UUID('43ca3083-fd01-4ecf-a6b3-910c5ecbcf59'), name='Pragna Gopa', primary_email=None,
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Pragna Gopa <pragna.gopa@hotmail.com>', aliases=None,
                                name='Pragna Gopa', email='pragna.gopa@hotmail.com',
                                user_id=UUID('43ca3083-fd01-4ecf-a6b3-910c5ecbcf59'))])],
                 User(id=UUID('42c6535e-aee1-4105-8a6e-5b3507048d6d'), name='Abhishek Kumar', primary_email=None,
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Abhishek Kumar <abhiku@microsoft.com>', aliases=None,
                                name='Abhishek Kumar', email='abhiku@microsoft.com',
                                user_id=UUID('42c6535e-aee1-4105-8a6e-5b3507048d6d'))]),
                 User(id=UUID('42d3f9e6-f031-4546-9f07-a99c66e77f70'), name='Adrian Hall', primary_email=None,
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Adrian Hall <adrian@shellmonger.com>', aliases=None, name='Adrian Hall',
                                email='adrian@shellmonger.com', user_id=UUID('42d3f9e6-f031-4546-9f07-a99c66e77f70'))]),
                 User(id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1'), name='Alexey Rodionov', primary_email='alrod@microsoft.com',
                      is_active=True, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Alexey Rodionov <alrod@microsoft.com>', aliases=None,
                                name='Alexey Rodionov', email='alrod@microsoft.com',
                                user_id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1'))]),
                 [User(id=UUID('7a103b20-67d3-4656-8bb5-fc5c1ef353d4'), name='Donna Malayeri', primary_email=None,
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>', aliases=None,
                                name='Donna Malayeri', email='DonnaM@Donnas-MacBook-Air.local',
                                user_id=UUID('7a103b20-67d3-4656-8bb5-fc5c1ef353d4'))]),
                 User(id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c'), name='Donna Malayeri', primary_email=None,
                      is_active=True, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Donna Malayeri <DonnaM@erik_winters.northamerica.corp.microsoft.com>',
                                aliases=None, name='Donna Malayeri',
                                email='DonnaM@erik_winters.northamerica.corp.microsoft.com',
                                user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
                         Author(canonical_name='Donna Malayeri <DonnaM@jimwan-carbon.northamerica.corp.microsoft.com>',
                                aliases=None, name='Donna Malayeri',
                                email='DonnaM@jimwan-carbon.northamerica.corp.microsoft.com',
                                user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c'))]),
                 User(id=UUID('6880c4a0-877f-4523-a3da-9906097a533e'), name='Donna Malayeri', primary_email=None,
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Donna Malayeri <DonnaM@mattshel-asus.redmond.corp.microsoft.com>',
                                aliases=None, name='Donna Malayeri',
                                email='DonnaM@mattshel-asus.redmond.corp.microsoft.com',
                                user_id=UUID('6880c4a0-877f-4523-a3da-9906097a533e'))]),
                 User(id=UUID('3930c9ff-29b5-48e9-860f-bd3eb05009ab'), name='Donna Malayeri', primary_email=None,
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Donna Malayeri <donnam@microsoft.com>', aliases=None,
                                name='Donna Malayeri', email='donnam@microsoft.com',
                                user_id=UUID('3930c9ff-29b5-48e9-860f-bd3eb05009ab'))])]]
        users_merged_count, authors_merged_count = merge_users(users)
        self.assertEqual(4, users_merged_count)
        self.assertEqual(4,authors_merged_count)

        expected = [
                    [User(id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'), name='Pragna Gopa', primary_email=None,
                          is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                          is_show_email=True, identities=[
                            Author(canonical_name='Pragna Gopa <pgopa@microsoft.com>', aliases=None, name='Pragna Gopa',
                                   email='pgopa@microsoft.com', user_id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10')),
                            Author(canonical_name='Pragna Gopa <pragna.gopa@hotmail.com>', aliases='1', name='Pragna Gopa',
                                   email='pragna.gopa@hotmail.com', user_id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'))])],
                    User(id=UUID('42c6535e-aee1-4105-8a6e-5b3507048d6d'), name='Abhishek Kumar', primary_email=None,
                         is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                         is_show_email=True, identities=[
                            Author(canonical_name='Abhishek Kumar <abhiku@microsoft.com>', aliases=None,
                                   name='Abhishek Kumar', email='abhiku@microsoft.com',
                                   user_id=UUID('42c6535e-aee1-4105-8a6e-5b3507048d6d'))]),
                    User(id=UUID('42d3f9e6-f031-4546-9f07-a99c66e77f70'), name='Adrian Hall', primary_email=None,
                         is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                         is_show_email=True, identities=[
                            Author(canonical_name='Adrian Hall <adrian@shellmonger.com>', aliases=None,
                                   name='Adrian Hall', email='adrian@shellmonger.com',
                                   user_id=UUID('42d3f9e6-f031-4546-9f07-a99c66e77f70'))]),
                    User(id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1'), name='Alexey Rodionov', primary_email='alrod@microsoft.com',
                         is_active=True, description=None, workplace=None, location=None, website=None, twitter=None,
                         is_show_email=True, identities=[
                            Author(canonical_name='Alexey Rodionov <alrod@microsoft.com>', aliases=None,
                                   name='Alexey Rodionov', email='alrod@microsoft.com',
                                   user_id=UUID('e0308b07-8de6-4e82-bf82-4121fd018ad1'))]),
                    [User(id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c'), name='Donna Malayeri', primary_email=None,
                          is_active=True, description=None, workplace=None, location=None, website=None, twitter=None,
                          is_show_email=True, identities=[
                            Author(canonical_name='Donna Malayeri <DonnaM@erik_winters.northamerica.corp.microsoft.com>', aliases=None, name='Donna Malayeri', email='DonnaM@erik_winters.northamerica.corp.microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
                            Author(canonical_name='Donna Malayeri <DonnaM@jimwan-carbon.northamerica.corp.microsoft.com>', aliases=None, name='Donna Malayeri', email='DonnaM@jimwan-carbon.northamerica.corp.microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
                            Author(canonical_name='Donna Malayeri <donnam@microsoft.com>', aliases='1', name='Donna Malayeri', email='donnam@microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
                            Author(canonical_name='Donna Malayeri <DonnaM@mattshel-asus.redmond.corp.microsoft.com>', aliases='1', name='Donna Malayeri', email='DonnaM@mattshel-asus.redmond.corp.microsoft.com', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')),
                            Author(canonical_name='Donna Malayeri <DonnaM@Donnas-MacBook-Air.local>', aliases='1', name='Donna Malayeri', email='DonnaM@Donnas-MacBook-Air.local', user_id=UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c'))])]]

        self.assertListEqual(expected, users)

    def test_merge_users_set_longest_name_of_all_authors(self):

        users = [
                [User(id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'), name='B', primary_email='264380+bartosz-lipinski@users.noreply.github.com',
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                        Author(canonical_name='B <264380+bartosz-lipinski@users.noreply.github.com>',
                               aliases=None, name='B', email='264380+bartosz-lipinski@users.noreply.github.com',
                               user_id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'))]),
                User(id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'), name='Bartosz Lipinski', primary_email='264380+bartosz-lipinski@users.noreply.github.com',
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Bartosz Lipinski <264380+bartosz-lipinski@users.noreply.github.com>',
                                aliases=None, name='Bartosz Lipinski', email='264380+bartosz-lipinski@users.noreply.github.com',
                                user_id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'))])]]
        users_merged_count, authors_merged_count = merge_users(users)
        self.assertEqual(1, users_merged_count)
        self.assertEqual(1,authors_merged_count)

        expected = [
                    [User(id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'), name='Bartosz Lipinski', primary_email='264380+bartosz-lipinski@users.noreply.github.com',
                          is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                          is_show_email=True, identities=[
                            Author(canonical_name='Bartosz Lipinski <264380+bartosz-lipinski@users.noreply.github.com>',
                                   aliases=None, name='Bartosz Lipinski',
                                   email='264380+bartosz-lipinski@users.noreply.github.com',
                                   user_id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6')),
                            Author(canonical_name='B <264380+bartosz-lipinski@users.noreply.github.com>',
                                   aliases='1', name='B', email='264380+bartosz-lipinski@users.noreply.github.com',
                                   user_id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'))
                        ])]]

        self.assertListEqual(expected, users)

    def test_merge_users_set_longest_name_of_all_authors_manual_confirmation(self):

        users = [
                [User(id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'), name='B', primary_email='264380+bartosz-lipinski@users.noreply.github.com',
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                        Author(canonical_name='B <264380+bartosz-lipinski@users.noreply.github.com>',
                               aliases=None, name='B', email='264380+bartosz-lipinski@users.noreply.github.com',
                               user_id=UUID('0eb24dea-a3a0-4e28-8dd8-3e9332cabe10'))]),
                User(id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'), name='Bartosz Lipinski', primary_email='264380+bartosz-lipinski@users.noreply.github.com',
                      is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                      is_show_email=True, identities=[
                         Author(canonical_name='Bartosz Lipinski <264380+bartosz-lipinski@users.noreply.github.com>',
                                aliases=None, name='Bartosz Lipinski', email='264380+bartosz-lipinski@users.noreply.github.com',
                                user_id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'))])]]
        users_merged_count, authors_merged_count = merge_users(users, get_bool_input)
        self.assertEqual(1, users_merged_count)
        self.assertEqual(1,authors_merged_count)

        expected = [
                    [User(id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'), name='Bartosz Lipinski', primary_email='264380+bartosz-lipinski@users.noreply.github.com',
                          is_active=False, description=None, workplace=None, location=None, website=None, twitter=None,
                          is_show_email=True, identities=[
                            Author(canonical_name='Bartosz Lipinski <264380+bartosz-lipinski@users.noreply.github.com>',
                                   aliases=None, name='Bartosz Lipinski',
                                   email='264380+bartosz-lipinski@users.noreply.github.com',
                                   user_id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6')),
                            Author(canonical_name='B <264380+bartosz-lipinski@users.noreply.github.com>',
                                   aliases='1', name='B', email='264380+bartosz-lipinski@users.noreply.github.com',
                                   user_id=UUID('fe3c6550-6779-4b8a-b350-68a061cffdb6'))
                        ])]]

        self.assertListEqual(expected, users)

    def test_identities_updater_add_authors_to_existing_user_blacklisted_domains(self):

        authors = {
            'Jenny Cooper <deploy@travis-ci.org>':
                Author(canonical_name='Jenny Cooper <deploy@travis-ci.org>', aliases=None,
                        name='Jenny Cooper', email='deploy@travis-ci.org', user_id=None),
            'Fergal Connolly <deploy@travis-ci.org>':
                Author(canonical_name='Fergal Connolly <deploy@travis-ci.org>', aliases=None,
                       name='Fergal Connolly', email='deploy@travis-ci.org', user_id=None),
            'Clarity Team <deploy@travis-ci.org>':
                Author(canonical_name='Clarity Team <deploy@travis-ci.org>', aliases=None,
                        name='Clarity Team', email='deploy@travis-ci.org', user_id=None),
            'Deployment Bot (from Travis CI) <deploy@travis-ci.org>':
                Author(canonical_name='Deployment Bot (from Travis CI) <deploy@travis-ci.org>', aliases=None,
                        name='Deployment Bot (from Travis CI)', email='deploy@travis-ci.org', user_id=None)
            }

        for author in authors.values():
            try:
                save_new_author(author.canonical_name)
            except Exception as e:
                print('Author: {}'.format(e))

        # remove the last author
        last_author = authors.popitem()
        # create user for one of the authors
        user = User(name=last_author[1].name,
                       primary_email=last_author[1].email,
                       is_active=True)
        create_new_user(user)

        len_matched_users_by_email, len_matched_users_by_email_and_name, len_users, len_authors, matched_users_by_email_and_name, users_merged_count, authors_merged_count = identify_authors_to_merge(
            authors)

        authors_updated, users_inserted = save_identified_merged_users(matched_users_by_email_and_name)

        self.assertEqual(0, len_users)
        self.assertEqual(3, len_authors)
        self.assertEqual(0, len_matched_users_by_email)
        self.assertEqual(0, len_matched_users_by_email_and_name)
        self.assertEqual(0, users_merged_count)
        self.assertEqual(0, authors_merged_count)
        self.assertEqual(0, users_inserted)
        self.assertEqual(0, authors_updated)
        self.assertEqual(authors_merged_count, authors_updated)


if __name__ == '__main__':
    unittest.main()
