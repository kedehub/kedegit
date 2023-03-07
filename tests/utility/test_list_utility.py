import unittest

from kedehub.services.dro.author_dto import Author
from kedehub.utility.list_utility import list_names, list_names_and_emails

class ListUtilityTestCase(unittest.TestCase):
    def test_list_names(self):

        authors = [Author(canonical_name='J. Smith <>', name='J. Smith', email=''),
                                 Author(canonical_name='John Smith <>', name='John Smith', email=''),
                                 Author(canonical_name=' <>', name='', email=''),
                                 Author(canonical_name=' <jsmith>', name='', email='jsmith')]

        names = list_names(authors)
        self.assertListEqual(['J. Smith', 'John Smith', '', ''],names)

    def test_list_names_and_emails(self):

        authors = [Author(canonical_name='J. Smith <>', name='J. Smith', email='jsmith@example.net'),
                                 Author(canonical_name='John Smith <>', name='John Smith', email=''),
                                 Author(canonical_name=' <>', name='', email='jsmith'),
                                 Author(canonical_name=' <jsmith>', name='', email='jsmith@example.com')]

        names_and_emails = list(list_names_and_emails(authors))

        self.assertListEqual(['J. Smith', 'jsmith', 'John Smith', '', '', 'jsmith', '', 'jsmith'],names_and_emails)

    def test_list_names_and_emails_no_list_identity(self):

        authors = Author(canonical_name='J. Smith <>', name='J. Smith', email='jsmith@example.net')

        names_and_emails = list(list_names_and_emails(authors))

        self.assertListEqual(['J. Smith', 'jsmith'],names_and_emails)

if __name__ == '__main__':
    unittest.main()
