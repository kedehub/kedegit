import requests
from requests.auth import HTTPBasicAuth
import json

class BitbucketClient:

    def __init__(self, workspace_id: str, username: str, password: str):
        self.workspace_id = workspace_id
        self.username = username
        self.password = password

    def get_repos(self):

        bitbucket_api_root = 'https://api.bitbucket.org/2.0/repositories/'
        repo_names = list()
        next_page_url = bitbucket_api_root + self.workspace_id
        while next_page_url is not None:
            raw_request = requests.get(next_page_url, auth=HTTPBasicAuth(self.username, self.password))
            dict_request = json.loads(raw_request.content.decode('utf-8'))
            repos = dict_request['values']
            # https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D
            for repo in repos:
                for url in repo["links"]["clone"]:
                    if (url["name"] == "https"):
                        repo_names.append(url['href'])

            next_page_url = dict_request.get('next', None)
        return repo_names