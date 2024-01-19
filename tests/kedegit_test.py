import os
import time
import unittest
from kedehub.kedegit import KedeGit
from kedehub.services.commit_service import get_commits_per_project
from tests import working_directory
import subprocess

class KedeGitTest(unittest.TestCase):

    _main_repo_initial_commit_hexsha = 'c153f2881f0f0025a9ff5754e74111333ce859cd'
    _main_repo_second_commit_hexsha = '5151985f7e3551c73ccb65cda2b021194b30b30a'
    _main_repo_test_commit_hexsha = 'c80ee8a32baaee8df8133b8afca26d63d857684e'
    _main_repo_head_commit_hexsha = '74e48c8686b26dc644951b55717e8828eb704587'

    def _fetch_commit(self, hexsha, kedegit=None):
        if kedegit is None:
            kedegit = self.kedegit
        return next(c for c in get_commits_per_project(kedegit.project_name, kedegit._shas_to_commits) if c.hexsha == hexsha)

    def _make_kedegit(self, project_name):
        return KedeGit(project_name)

    def setUp(self):
        print()
        print(self.id())
        self.current_directory = os.path.abspath(os.path.dirname(__file__))
        self.working_directory = working_directory
        self.proc = subprocess.Popen(['/Users/dimitarbakardzhiev/git/kedehub_server/venv311/bin/python3', '-m' ,'tests'],
                                     cwd = '/Users/dimitarbakardzhiev/git/kedehub_server/',
                                     stdin=subprocess.PIPE)
        time.sleep(5.5)
        self.kedegit = self._make_kedegit('test')

    def tearDown(self):
        self.proc.communicate(input=b"stop", timeout=5)
        self.proc.terminate()
        time.sleep(5.5)