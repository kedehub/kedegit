import os
import unittest
from tests.kedehub_test_load_db_once import KedeHubLoadDBOnceTest
from kedehub.services.kede_service import calculate_kede_for_person, calculate_weekly_kede_for_person, \
    delete_kede_for_repo


class KedeGitKedeServiceTest(KedeHubLoadDBOnceTest):

    @classmethod
    def setUpClass(cls):
        super(KedeGitKedeServiceTest, cls).setUpClass()
        cls.kedegit.add_repository(os.path.join(cls.current_directory, '../tests/data', 'azbg_virtual_pos'),
                                    os.path.join(cls.current_directory, '../tests/data', 'azbg_virtual_pos-config.json'))

    @classmethod
    def tearDownClass(cls):
        super(KedeGitKedeServiceTest, cls).tearDownClass()

    def test_calculate_kede_for_pwrson(self):
        project = 'azbg_virtual_pos'
        calculate_kede_for_person(project,'Dimitar <dimitar>')

    def test_calculate_weekly_kede_for_pwrson(self):
        project = 'azbg_virtual_pos'
        calculate_weekly_kede_for_person(project, 'Dimitar <dimitar>')

    def test_delete_kede_for_repo(self):
        delete_kede_for_repo(1)

if __name__ == '__main__':
    unittest.main()
