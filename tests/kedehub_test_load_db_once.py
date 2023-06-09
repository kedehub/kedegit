import os
import unittest
import time
from kedehub.kedegit import KedeGit
from kedehub.services.commit_service import get_commits_per_project
from tests import working_directory
import subprocess


class KedeHubLoadDBOnceTest(unittest.TestCase):

    _main_repo_initial_commit_hexsha = 'c153f2881f0f0025a9ff5754e74111333ce859cd'
    _main_repo_second_commit_hexsha = '5151985f7e3551c73ccb65cda2b021194b30b30a'
    _main_repo_test_commit_hexsha = 'c80ee8a32baaee8df8133b8afca26d63d857684e'
    _main_repo_head_commit_hexsha = '74e48c8686b26dc644951b55717e8828eb704587'

    def _fetch_commit(self, hexsha, kedegit=None):
        if kedegit is None:
            kedegit = self.kedegit
        return next(c for c in get_commits_per_project(kedegit.project_name, kedegit._shas_to_commits) if c.hexsha == hexsha)

    @classmethod
    def setUpClass(cls):
        cls.current_directory = os.path.abspath(os.path.dirname(__file__))
        cls.working_directory = working_directory
        cls.proc = subprocess.Popen(['/Users/dimitarbakardzhiev/git/kedehub_server//venv39/bin/python', '-m' ,'tests'],
                                     cwd = '/Users/dimitarbakardzhiev/git/kedehub_server/',
                                     stdin=subprocess.PIPE)
        time.sleep(5.5)
        cls.kedegit = KedeGit('test')

    @classmethod
    def tearDownClass(cls):
        cls.proc.communicate(input=b"stop", timeout=5)
        cls.proc.terminate()
        time.sleep(5.5)