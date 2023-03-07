import os
import unittest
from tests.kedegit_test import KedeGitTest
from kedehub.services.dro.author_dto import Author
from kedehub.services.dro.repository_dto import Repository


class TestCommitObject(KedeGitTest):

    # Test the initial commit which parent is always "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    # git log --shortstat 8ab12bcd4562a12d78a65eeac6bbf97257ef02bf
    def test_create_commit_object_first_commit(self):
        repository_path = os.path.join(self.current_directory, '../tests/data',
                                       'azbg_virtual_pos')
        configuration_file_path = os.path.join(self.current_directory, '../tests/data',
                                               'azbg_virtual_pos-config.json')
        dbrepo = Repository(id = 1,origin = "http://git.elando.bg/eLando/azbg_virtual_pos.git", repository_path=repository_path, configuration_file_path=configuration_file_path)
        dbrepo._init_properties()
        commit = dbrepo.git_repository.commit('8ab12bcd4562a12d78a65eeac6bbf97257ef02bf')
        author_line = 'Dimitar <dimitar>'
        author = Author(canonical_name=author_line, name = 'X', email = 'x@y.com')
        self.kedegit._names_to_authors[author_line] = author
        commit_object = self.kedegit._create_commit_object(dbrepo, commit, author.canonical_name)

        self.assertEqual(901, commit_object.added_lines)
        self.assertEqual(24009, commit_object.added_chars)
        self.assertEqual(0, commit_object.deleted_lines)
        self.assertEqual(0, commit_object.deleted_chars)
        self.assertEqual(0,len(commit_object.parent_ids))
        self.assertEqual({'Configuration': 5586, 'Java': 18423}, commit_object.lang_count)
        self.assertEqual(commit_object.added_chars, commit_object.lang_count['Java'] + commit_object.lang_count['Configuration'])

    # Tets if the proper parent SHA is assigned : b5f9d156782ee9252ffb06d9fc94ded8d8b80b3f
    # git log --shortstat b5f9d156782ee9252ffb06d9fc94ded8d8b80b3f
    def test_create_commit_object_small_commit(self):
        repository_path = os.path.join(self.current_directory, '../tests/data',
                                       'azbg_virtual_pos')
        configuration_file_path = os.path.join(self.current_directory, '../tests/data',
                                               'azbg_virtual_pos-config.json')
        dbrepo = Repository(id = 1,origin = "http://git.elando.bg/eLando/azbg_virtual_pos.git", repository_path=repository_path, configuration_file_path=configuration_file_path)
        dbrepo._init_properties()
        commit = dbrepo.git_repository.commit('b5f9d156782ee9252ffb06d9fc94ded8d8b80b3f')
        author_line = 'Dimitar <dimitar>'
        author = Author(canonical_name=author_line, name = 'X', email = 'x@y.com')
        self.kedegit._names_to_authors[author_line] = author
        commit_object = self.kedegit._create_commit_object(dbrepo, commit, author.canonical_name)

        self.assertEqual(6, commit_object.added_lines)
        self.assertEqual(8, commit_object.added_chars)
        self.assertEqual(4, commit_object.deleted_lines)
        self.assertEqual(32, commit_object.deleted_chars)
        self.assertEqual('cb70c2e9140dbb639b3a7a964dde7a224fc4338f',commit_object.parent_ids)
        self.assertEqual({'Java': 8}, commit_object.lang_count)
        self.assertEqual(commit_object.added_chars, commit_object.lang_count['Java'])

if __name__ == '__main__':
    unittest.main()
