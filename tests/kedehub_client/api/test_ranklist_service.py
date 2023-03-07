import datetime
import os
import unittest
from tests.kedegit_test import KedeGitTest
from kedehub.services.kede_service import calculate_kede_for_person, \
    calculate_weekly_kede_for_person
from kedehub.services.ranklist_service import load_rank_for_people, calculate_rank


class KedeHubRanklistServiceTest(KedeGitTest):

    def setUp(self):
        super().setUp()
        self.start_date = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.kedegit.add_repository(os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos'),
                                    os.path.join(self.current_directory, '../tests/data', 'azbg_virtual_pos-config.json'),
                                    earliest_date=self.start_date)

        calculate_kede_for_person(self.kedegit.project_name, 'Dimitar <dimitar>')
        calculate_weekly_kede_for_person(self.kedegit.project_name, 'Dimitar <dimitar>')

    def tearDown(self):
        super().tearDown()

    def test_load_rank(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        calculate_rank(None, today)
        people_to_show = 'Dimitar <dimitar>'
        expected_json = [{'author_name': 'Dimitar <dimitar>', 'rank': '0.0', 'week_date': '2020-04-13'},
                     {'author_name': 'Dimitar <dimitar>',
                      'rank': '50.0',
                      'week_date': '2020-04-20'},
                     {'author_name': 'Dimitar <dimitar>', 'rank': '0.0', 'week_date': '2020-04-27'},
                     {'author_name': 'Dimitar <dimitar>',
                      'rank': '50.0',
                      'week_date': '2020-05-04'}]
        actual_json = load_rank_for_people(people_to_show, datetime.date(2020, 1, 1), None)

        self.assertEqual(expected_json, actual_json)

    def test_calculate_rank(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        calculate_rank(None, today)


if __name__ == '__main__':
    unittest.main()
