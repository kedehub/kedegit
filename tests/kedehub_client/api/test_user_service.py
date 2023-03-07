import datetime
import os
import unittest
from tests.kedegit_test import KedeGitTest
from pydantic import EmailStr
from kedehub.services.dro.user_dto import User
from kedehub.services.user_service import create_new_user


class UserServiceTestCase(KedeGitTest):

    def setUp(self):
        super().setUp()
        self.cloned_worktree = os.path.join(self.working_directory.name, 'worktree')
        self.start_date = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos'),
                                    os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json'),
                                    earliest_date=self.start_date)

    def tearDown(self):
        super().tearDown()

    def test_create_user(self):

        expected_user_to_create = User(
            name='test_user',
            primary_email=EmailStr('atanas.atanasov@elando.bg')
        )

        created_user = create_new_user(expected_user_to_create)
        self.assertEqual(expected_user_to_create.name, created_user.name)
        self.assertEqual(expected_user_to_create.primary_email, created_user.primary_email)
        self.assertTrue(created_user.is_show_email)


if __name__ == '__main__':
    unittest.main()
