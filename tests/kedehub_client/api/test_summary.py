import datetime
import os
import unittest
from tests.kedegit_test import KedeGitTest
from kedehub.services.commit_service import get_project_commits


class KedeGitSummaryTest(KedeGitTest):

    def setUp(self):
        super().setUp()
        self.cloned_worktree = os.path.join(self.working_directory.name, 'worktree')
        self.start_date = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos'),
                                    os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json'),
                                    earliest_date=self.start_date)

    def tearDown(self):
        super().tearDown()

    def test_iter_project_commits(self):
        commit_counts = {}
        for commit in get_project_commits('test'):
            commit_counts[commit.author_name] = commit_counts.get(commit.author_name, 0) + 1
        self.assertEqual(64, commit_counts['Dimitar <dimitar>'])
        self.assertEqual(34, commit_counts['Atanas Atanasov <atanas.atanasov@elando.bg>'])
        self.assertEqual(24, commit_counts['Edward Kuiumdjian <edward.kuiumdjian@elando.bg>'])

if __name__ == '__main__':
    unittest.main()
