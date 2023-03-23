from gitea_client import Token, GiteaApi
from urllib.parse import urlparse, urlsplit, urlunsplit

class GogsClient:

    def __init__(self, host: str, token: str, username: str):
        self.host = host
        self.token = token
        self.username = username

    def get_repos(self):
        token = Token(self.token)
        api = GiteaApi(self.host)
        repos = api.get_user_repos(token, self.username)
        repo_names = list()
        for repo in repos:
            repo_names.append(self.replace_port(repo.urls.clone_url))
        return repo_names

    def replace_port(self, repo):
        parsed_url = urlparse(repo)
        url = list(urlsplit(parsed_url.geturl()))
        url[1] = parsed_url.hostname
        clone_url = urlunsplit(url)
        return clone_url