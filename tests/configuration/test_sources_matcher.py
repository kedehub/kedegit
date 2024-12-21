import os
import unittest

from kedehub.configuration.sources_matcher import match


class SourceMatcherTest(unittest.TestCase):

    def test_plain_pattern_matches_equal_file(self):
        self.assertTrue(match('dir/file.txt', os.path.join('dir', 'file.txt')))

    def test_plain_pattern_does_not_match_unequal_file(self):
        self.assertFalse(match('dir/file.txt', os.path.join('dir', 'file.csv')))

    def test_plain_pattern_requires_full_match(self):
        self.assertFalse(match('file.txt', os.path.join('dir', 'file.txt')))

    def test_trailing_slash_ignored_in_pattern(self):
        self.assertTrue(match('dir/file/', os.path.join('dir', 'file')))

    def test_trailing_slash_ignored_in_file_name(self):
        self.assertTrue(match('dir/file', os.path.join('dir', 'file', '')))

    def test_leading_slash_in_pattern_required_to_match(self):
        self.assertFalse(match('/dir/file.txt', os.path.join('dir', 'file.txt')))

    def test_leading_slash_in_file_name_required_to_match(self):
        self.assertFalse(match('dir/file.txt', os.path.join(os.sep, 'dir', 'file.txt')))

    def test_question_matches_one_character(self):
        self.assertTrue(match('dir/fil?.txt', os.path.join('dir', 'file.txt')))

    def test_question_does_not_match_multiple_characters(self):
        self.assertFalse(match('dir/fi?.txt', os.path.join('dir', 'file.txt')))

    def test_question_does_not_match_path_separator(self):
        self.assertFalse(match('dir?file.txt', os.path.join('dir', 'file.txt')))

    def test_star_matches_any_characters(self):
        self.assertTrue(match('dir/*.txt', os.path.join('dir', 'file.txt')))

    def test_star_matches_zero_characters(self):
        self.assertTrue(match('dir/file*.txt', os.path.join('dir', 'file.txt')))

    def test_star_does_not_match_path_separator(self):
        self.assertFalse(match('di*ile.txt', os.path.join('dir', 'file.txt')))

    def test_doublestar_matches_multiple_directories(self):
        self.assertTrue(match('dir/**/file.txt', os.path.join('dir', 'dir1', 'dir2', 'file.txt')))

    def test_doublestar_matches_zero_directories(self):
        self.assertTrue(match('dir/**/file.txt', os.path.join('dir', 'file.txt')))

    def test_doublestar_matches_in_the_beginning(self):
        self.assertTrue(match('**/file.txt', os.path.join('dir', 'dir1', 'file.txt')))

    def test_doublestar_matches_in_the_end(self):
        self.assertTrue(match('dir/**', os.path.join('dir', 'dir1', 'file.txt')))

    def test_only_doublestar_in_pattern_matches(self):
        self.assertTrue(match('**', os.path.join('dir', 'dir1', 'file.txt')))

    def test_doublestar_not_allowed_with_other_content(self):
        with self.assertRaises(ValueError):
            match('dir/**1/file.txt', os.path.join('dir', 'dir1', 'dir2', 'file.txt'))

    def test_repeated_doublestars_match(self):
        self.assertTrue(match('dir/**/**/file.txt', os.path.join('dir', 'file.txt')))

    def test_star_question_multiple_doublestar_matches(self):
        self.assertTrue(
            match('d*/**/dir3/**/fil?.txt', os.path.join('dir', 'dir1', 'dir2', 'dir3', 'dir4', 'dir5', 'file.txt')))

    def test_matches_any_character_in_seq(self):
        self.assertTrue(match('dir/[fxyz]ile.txt', os.path.join('dir', 'file.txt')))

    def test_matches_no_character_in_seq(self):
        self.assertFalse(match('dir/[fxyz]ile.txt', os.path.join('dir', 'cile.txt')))

    def test_regex_wildcard_only_matches_literally(self):
        self.assertFalse(match('dir/file.txt', os.path.join('dir', 'file_txt')))

    def test_quastion_mark__matches_in_the_middle_of_file_names(self):
        self.assertTrue(match('dir/f?le.txt', os.path.join('dir', 'f?le.txt')))

    def test_single_star_matches_in_the_beginning_of_file_names(self):
        self.assertTrue(match('dir/*le.txt', os.path.join('dir', '*file.txt')))

    def test_doublestar_matches_in_the_beginning_and_star_for_file_names(self):
        self.assertTrue(match('**/*.txt', os.path.join('dir', 'dir1', 'file.txt')))

    def test_twice_doublestar_matches_in_the_beginning_and_no_star_for_file_names(self):
        self.assertTrue(match('**/**/file.txt', os.path.join('dir', 'dir1','dir2','dir3','dir4', 'file.txt')))

    def test_twice_doublestar_matches_in_the_beginning_and_star_for_file_names(self):
        self.assertTrue(match('**/**/*.txt', os.path.join('dir', 'dir1','dir2','dir3', 'file.txt')))

    def test_twice_doublestar_matches_in_the_beginning_and_star_for_file_names_with_two_dots(self):
        self.assertTrue(match('**/**/*.min.css', os.path.join('dir', 'dir1','dir2','dir3', 'file.min.css')))

    def test_all_stars_for_file_name_with_two_dots(self):
        self.assertTrue(match('**/**/*', os.path.join('dir', 'dir1','dir2','dir3', 'file.min.css')))

if __name__ == '__main__':
    unittest.main()
