from github import Github, Auth
from github.PaginatedList import PaginatedList

class GithubClient:

    def __init__(self, token: str, organization: str):
        self.token = token
        self.organization = organization

    def get_repos(self):
        # https://pygithub.readthedocs.io/en/latest/utilities.html#pagination
        g = Github(auth=Auth.Token(self.token))
        org = g.get_organization(self.organization)
        repos = org.get_repos()

        repo_names = [repo.clone_url for repo in repos]
        return repo_names