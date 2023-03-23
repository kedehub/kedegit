import os

import unittest

from unidiff import PatchSet

from kedehub.config import Configuration
from kedehub.git.git_utility import _make_diffed_commit_char_stats, get_git_repository, \
    count_added_deleted_chars_simplest_levenstein


class TestDiff(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.abspath(os.path.dirname(__file__))

    def test_make_diffed_commit_char_stats_big_commit(self):
        repository_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos')
        configuration_file_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos-config.json')
        brepo = get_git_repository(repository_path)
        commit = brepo.commit('cb70c2e9140dbb639b3a7a964dde7a224fc4338f')
        parent_commit = commit.parents[0]
        lines_added,lines_deleted,chars_aded,chars_deleted, lang_counter = _make_diffed_commit_char_stats(commit,
                                                                                            parent_commit,
                                                                                            Configuration(configuration_file_path))

        self.assertEqual(731,lines_added)
        self.assertEqual(382,lines_deleted)
        self.assertEqual(17886, chars_aded)
        self.assertEqual(8237, chars_deleted)
        self.assertEqual({'Configuration': 393, 'Java': 17493},lang_counter)
        self.assertEqual(chars_aded,lang_counter['Java']+lang_counter['Configuration'])

    def test_make_diffed_commit_char_stats_small_commit(self):
        repository_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos') #os.path.abspath('/Users/dimitarbakardzhiev/git//azbg_virtual_pos/')
        configuration_file_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos-config.json') #os.path.join(repository_path, 'git-kedegit-config.json')
        brepo = get_git_repository(repository_path)
        commit = brepo.commit('b5f9d156782ee9252ffb06d9fc94ded8d8b80b3f')
        parent_commit = commit.parents[0]
        lines_added,lines_deleted,chars_aded,chars_deleted, lang_counter = _make_diffed_commit_char_stats(commit,
                                                                                            parent_commit,
                                                                                            Configuration(configuration_file_path))
        self.assertEqual(6,lines_added)
        self.assertEqual(4,lines_deleted)
        self.assertEqual(8, chars_aded)
        self.assertEqual(32, chars_deleted)
        self.assertEqual({'Java': 8},lang_counter)
        self.assertEqual(chars_aded, lang_counter['Java'])

    def test_make_diffed_commit_char_stats_small_commit_1(self):
        configuration_file_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos-config.json') #os.path.join(repository_path, 'git-kedegit-config.json')
        repository_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos')
        brepo = get_git_repository(repository_path)
        commit = brepo.commit('dd45824698189d7ec9a78b1de8b2305f3fdb2fcd')
        parent_commit = commit.parents[0]
        lines_added,lines_deleted,chars_aded,chars_deleted, lang_counter = _make_diffed_commit_char_stats(commit,
                                                                                            parent_commit,
                                                                                            Configuration(configuration_file_path))
        self.assertEqual(7,lines_added)
        self.assertEqual(6,lines_deleted)
        self.assertEqual(115, chars_aded)
        self.assertEqual(53, chars_deleted)
        self.assertEqual({'Text': 60, 'Java': 55},lang_counter)
        self.assertEqual(chars_aded, lang_counter['Java'] + lang_counter['Text'])

    def test_make_diffed_commit_char_stats_first_commit(self):
        repository_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos')
        configuration_file_path = os.path.join(self.current_directory, '../data', 'azbg_virtual_pos-config.json')
        brepo = get_git_repository(repository_path)
        commit = brepo.commit('8ab12bcd4562a12d78a65eeac6bbf97257ef02bf')
        EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
        parent_commit = brepo.tree(EMPTY_TREE_SHA)
        lines_added, lines_deleted, chars_aded, chars_deleted, lang_counter = _make_diffed_commit_char_stats(commit,
                                                                                               parent_commit,
                                                                                               Configuration(configuration_file_path))
        self.assertEqual(901, lines_added)
        self.assertEqual(0, lines_deleted)
        self.assertEqual(24009, chars_aded)
        self.assertEqual(0, chars_deleted)
        self.assertEqual({'Configuration': 5586, 'Java': 18423},lang_counter)
        self.assertEqual(chars_aded, lang_counter['Java'] + lang_counter['Configuration'])

    def test__make_diffed_commit_char_stats__from_samples_pom_xml(self):
        utf8_file = os.path.join(self.current_directory, 'samples/pom.xml.diff')
        with open(utf8_file, 'rb') as diff_file:
            patch = PatchSet(diff_file, encoding='utf-8')

        # one file in the patch
        self.assertEqual(len(patch), 1)
        # one hunk in the patch
        self.assertEqual(len(patch[0]), 1)

        # file is modified
        self.assertTrue(patch[0].is_modified_file)
        self.assertFalse(patch[0].is_removed_file)
        self.assertFalse(patch[0].is_added_file)
        self.assertFalse(patch[0].is_binary_file)

        # Hunk 1: five additions, no deletions, a section header
        self.assertEqual(3, patch[0][0].added)
        self.assertEqual(3, patch[0][0].removed)

        patch_chars_aded, patch_chars_deleted = count_added_deleted_chars_simplest_levenstein(patch[0])

        self.assertEqual(45, patch_chars_aded)
        self.assertEqual(45,patch_chars_deleted)

    def test__make_diffed_commit_char_stats_solana_7ab3331f0104fb939b7148c6edc903fd94496841(self):
        # motivation https://github.com/solana-labs/solana/commit/7ab3331f0104fb939b7148c6edc903fd94496841
        utf8_file = os.path.join(self.current_directory, 'samples/solana_7ab3331f0104fb939b7148c6edc903fd94496841.diff')
        with open(utf8_file, 'rb') as diff_file:
            diffs = PatchSet(diff_file, encoding='utf-8')

        # four files in the diff
        self.assertEqual(4, len(diffs))
        # one hunk in the first diff
        self.assertEqual(1, len(diffs[0]))

        # file is modified
        self.assertTrue(diffs[0].is_modified_file)
        self.assertFalse(diffs[0].is_removed_file)
        self.assertFalse(diffs[0].is_added_file)
        self.assertFalse(diffs[0].is_binary_file)

        # First Hunk 1 of first file
        self.assertEqual(1, diffs[0][0].added)
        self.assertEqual(0, diffs[0][0].removed)

        patch_chars_aded, patch_chars_deleted = count_added_deleted_chars_simplest_levenstein(diffs[0])

        self.assertEqual(12, patch_chars_aded)
        self.assertEqual(0,patch_chars_deleted)

        patch_chars_aded, patch_chars_deleted = count_added_deleted_chars_simplest_levenstein(diffs[1])

        self.assertEqual(77, patch_chars_aded)
        self.assertEqual(30,patch_chars_deleted)

        patch_chars_aded, patch_chars_deleted = count_added_deleted_chars_simplest_levenstein(diffs[2])

        self.assertEqual(0, patch_chars_aded)
        self.assertEqual(11906,patch_chars_deleted)

        patch_chars_aded, patch_chars_deleted = count_added_deleted_chars_simplest_levenstein(diffs[3])

        self.assertEqual(13396, patch_chars_aded)
        self.assertEqual(0,patch_chars_deleted)


if __name__ == '__main__':
    unittest.main()