from gitlab import Gitlab

# https://stackoverflow.com/questions/29099456/how-to-clone-all-projects-of-a-group-at-once-in-gitlab

class GitlabClient:

    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token

    def get_repos(self):
        # https://python-gitlab.readthedocs.io/en/stable/api-usage.html
        gl = Gitlab(self.host, self.token)
        gl.auth()
        # https://python-gitlab.readthedocs.io/en/stable/api-usage.html#pagination
        projects = gl.projects.list(all=True)

        repo_names = list()
        for project in projects:
            repo_names.append(project.http_url_to_repo)
        return repo_names