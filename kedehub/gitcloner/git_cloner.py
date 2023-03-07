import os
from git import RemoteProgress
from git import Repo
import sys

from kedehub.git.git_utility import get_repo_name
from kedehub import server_config

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        # pbar = tqdm(total=max_count)
        # pbar.update(cur_count)
        print(cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

def clone_a_repo(clone_path, repo_clone_url):
    print('Cloning repo: {}'.format(repo_clone_url))
    try:
        # https://gitpython.readthedocs.io/en/stable/tutorial.html
        Repo.clone_from(repo_clone_url, clone_path, progress=CloneProgress())
        print('Cloning complete for repo {}'.format(repo_clone_url))
        return clone_path
    except Exception as e:
        print('Unable to clone repo {}. Reason: {} (exit code {})'.format(repo_clone_url, e.stderr, e.status))
        return False

class GitCloner:

    def __init__(self, workdir: str, api_client):
        self.workdir = workdir
        self.api_client = api_client
        print('Directory to clone to is:'+self.workdir)

    def clone_all(self):
        try:
            repo_clone_urls = self.load_repos()
        except Exception as e:
            print('FATAL: Could not get repos clone URLs: ({}). Terminating.'.format(e))
            sys.exit(1)

        number_or_repo_clone_urls = len(repo_clone_urls)
        repo_number = 1
        success_clone = 0

        for repo_clone_url in repo_clone_urls:
            # Folder name should be the repo_clone_url's name
            print('Cloning repo {} of {}'.format(repo_number, number_or_repo_clone_urls))

            if(self.clone_repo(repo_clone_url)):
                success_clone = success_clone + 1
            repo_number = repo_number + 1
        print('Successfully cloned {} out of {} repos'.format(success_clone, number_or_repo_clone_urls))

    def load_repos(self):
        print('Loading repos clone URLs...')
        repo_clone_urls = self.api_client.get_repos()
        number_or_repo_clone_urls = len(repo_clone_urls)
        print('Done: {} repos clone URLs loaded'.format(number_or_repo_clone_urls))
        return repo_clone_urls

    def clone_repo(self, repo_clone_url):
        repo_name = get_repo_name(repo_clone_url)
        clone_path = os.path.abspath(os.path.join(self.workdir, repo_name))
        if (os.path.exists(clone_path)):
            print('Skipping repo {} because path {} exists'.format(repo_clone_url, clone_path))
        elif (server_config.is_repo_present(repo_clone_url)):
            print('Skipping repo {} because path {} exists in config'.format(repo_clone_url, clone_path))
        else:
            return clone_a_repo(clone_path, repo_clone_url)


