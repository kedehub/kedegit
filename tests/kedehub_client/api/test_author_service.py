import datetime
import os
import unittest
from tests.kedegit_test import KedeGitTest
from kedehub.services.dro.author_dto import Author
from kedehub.services.author_service import load_authors_for_projects, save_new_author, \
    build_author_map, assign_author_to_user_profile
from kedehub_client import exceptions
from kedehub.git.git_utility import filter_invalid_unicode_sequences


class KedeGitAuthorServiceTest(KedeGitTest):

    def setUp(self):
        super().setUp()
        self.cloned_worktree = os.path.join(self.working_directory.name, 'worktree')
        self.start_date = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos'),
                                    os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json'),
                                    earliest_date=self.start_date)

    def tearDown(self):
        super().tearDown()

    def test_load_authors_for_projects(self):
        expected = ['Dimitar <dimitar>',
                 'Atanas Atanasov <atanas.atanasov@elando.bg>',
                 'Mincho Milev <mincho_pm@mail.bg>',
                 'Edward Kuiumdjian <edward.kuiumdjian@elando.bg>',
                 'JordanRadev <tyfp815@gmail.com>']
        persons = load_authors_for_projects([self.kedegit.project_name])
        self.assertEqual(expected, persons)

    def test_save_new_author(self):
        new_outhor = save_new_author('test_author <test@email.com>')
        expected = '{"canonical_name": "test_author <test@email.com>", "aliases": null, "name": "test_author", "email": "test@email.com", "user_id": null}'
        self.assertEqual(expected, new_outhor.json())

    def test_build_author_mapt(self):
        expected = {'Atanas Atanasov <atanas.atanasov@elando.bg>': Author(canonical_name='Atanas Atanasov <atanas.atanasov@elando.bg>', aliases=None, name='Atanas Atanasov', email='atanas.atanasov@elando.bg', user_id=None),
                 'Dimitar <dimitar>': Author(canonical_name='Dimitar <dimitar>', aliases=None, name='Dimitar', email='dimitar', user_id=None),
                 'Edward Kuiumdjian <edward.kuiumdjian@elando.bg>': Author(canonical_name='Edward Kuiumdjian <edward.kuiumdjian@elando.bg>', aliases=None, name='Edward Kuiumdjian', email='edward.kuiumdjian@elando.bg', user_id=None),
                 'JordanRadev <tyfp815@gmail.com>': Author(canonical_name='JordanRadev <tyfp815@gmail.com>', aliases=None, name='JordanRadev', email='tyfp815@gmail.com', user_id=None),
                 'Mincho Milev <mincho_pm@mail.bg>': Author(canonical_name='Mincho Milev <mincho_pm@mail.bg>', aliases=None, name='Mincho Milev', email='mincho_pm@mail.bg', user_id=None)}
        persons = build_author_map(self.kedegit.project_name)
        self.assertEqual(expected, persons)

    # def test_save_new_author_with_invalid_unicode_sequences(self):
    #     with self.assertRaises(exceptions.UnexpectedResponse,
    #                            msg="Unexpected Response: 500 (Internal Server Error)"):
    #         new_outhor = save_new_author('\udce5\udcae\udc9e\udce7\udc8e\udcb0 <test@email.com>')

    def test_save_new_author_with_invalid_unicode_sequences_filtered(self):
        new_outhor = save_new_author(filter_invalid_unicode_sequences('\udce5\udcae\udc9e\udce7\udc8e\udcb0 <test@email.com>'))

        self.assertEqual('实现', new_outhor.name)
        self.assertEqual('实现 <test@email.com>', new_outhor.canonical_name)

    def test_assign_author_to_user_profile(self):
        new_outhor = Author(canonical_name='Mincho Milev <mincho_pm@mail.bg>', aliases=None, name=' ', email=' ', user_id="94af6a7a-f60f-477f-aaf9-b88cc8a0f3d9")

        authors_updated = assign_author_to_user_profile(new_outhor)

        self.assertEqual(1, authors_updated)

if __name__ == '__main__':
    unittest.main()
