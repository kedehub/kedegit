from github import Github
from github.PaginatedList import PaginatedList

class GithubClient:

    def __init__(self, token: str, organization: str):
        self.token = token
        self.organization = organization

    def get_repos(self) -> PaginatedList:
        # https://pygithub.readthedocs.io/en/latest/utilities.html#pagination
        g = Github(self.token)
        org = g.get_organization(self.organization)
        repos = org.get_repos()

        # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
        repo_names = list()
        for repo in repos:
            repo_names.append(repo.clone_url)
        return repo_names