import unittest
from uuid import UUID

from kedehub.utility.email_utility import generate_no_reply_user_email_address


class EmailUtilityTestCase(unittest.TestCase):
    def test_generate_no_reply_user_email_address(self):
        id = UUID('8625eda0-c7bd-44c6-87df-c4a3b063d46c')
        username = 'test'
        email_address = generate_no_reply_user_email_address(id, username)
        self.assertEqual("8625eda0-c7bd-44c6-87df-c4a3b063d46c@users.noreply.kedegub.io", email_address)  # add assertion here


if __name__ == '__main__':
    unittest.main()
