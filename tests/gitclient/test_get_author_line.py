import unittest

from kedehub.gitclient.git_utility import filter_invalid_unicode_sequences

INVALID_UNICODE_STRING = '\udce5\udcae\udc9e\udce7\udc8e\udcb0'
INVALID_UNICODE_STRING_2 = 'H\udce5kon L\udcf8vdal <Hakon.Lovdal@ericsson.com>'

class KedeGitAuthorLineTest(unittest.TestCase):

    def test_filter_invalid_unicode_sequence(self):

        author_line = INVALID_UNICODE_STRING
        formatted = filter_invalid_unicode_sequences(author_line)
        self.assertEqual('实现', formatted)

    def test_NOT_filter_invalid_unicode_sequence(self):

        author_line = INVALID_UNICODE_STRING
        with self.assertRaises(UnicodeEncodeError, msg="'utf-8' codec can't encode characters in position 0-5: surrogates not allowed"):
            formatted = author_line.encode('utf8')

    def test_filter_invalid_unicode_sequence_2(self):
        author_line = INVALID_UNICODE_STRING_2
        formatted = filter_invalid_unicode_sequences(author_line)
        self.assertEqual('Håkon Løvdal <Hakon.Lovdal@ericsson.com>', formatted)

    def test_NOT_filter_invalid_unicode_sequence_2(self):
        author_line = INVALID_UNICODE_STRING_2
        with self.assertRaises(UnicodeEncodeError, msg="'utf-8' codec can't encode characters in position 0-5: surrogates not allowed"):
            formatted = author_line.encode('utf8')

if __name__ == '__main__':
    unittest.main()
