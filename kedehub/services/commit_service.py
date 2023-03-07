from kedehub_client import get_sync_apis
from kedehub_client.exceptions import UnexpectedResponse
import time

def save_new_commit(commit_dto):
    try:
        return get_sync_apis().commit_api.store_new_commit(commit_dto)
    except UnexpectedResponse:
        time.sleep(35)
        return 0


def get_commits_per_project(project_name, shas_to_commits):
    commits = []
    for dto_commit in get_sync_apis().commit_api.find_commits_per_project(project_name):
        selected_commit = shas_to_commits.get(dto_commit.hexsha)
        if selected_commit:
            commits.append(selected_commit)
    return commits

def get_project_commits(project_name):
    return get_sync_apis().commit_api.find_commits_per_project(project_name)

def build_commit_map(project_name):
    shas_to_commits = {}
    for dto_commit in get_sync_apis().commit_api.find_commits_per_project(project_name):
        shas_to_commits[dto_commit.hexsha] = dto_commit
    return shas_to_commits

def build_company_commit_map():
    shas_to_commits = {}
    for dto_commit in get_sync_apis().commit_api.get_commits_per_comoany():
        shas_to_commits[dto_commit.hexsha] = dto_commit
    return shas_to_commits

def find_last_commit_for_repository(repository_id):
    dto_commit = get_sync_apis().commit_api.find_last_commit_for_repository(repository_id)
    return dto_commit

def delete_commits_for_repository(repository_id):
    return get_sync_apis().commit_api.delete_repository_commits(repository_id)