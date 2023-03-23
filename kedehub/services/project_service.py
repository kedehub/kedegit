from kedehub_client import get_sync_apis

def assign_new_repo_to_existing_project(project_name, repository_id):
    return get_sync_apis().project_api.add_new_project_repository(project_name,repository_id)


def ensure_project_exists(project_name):
    return get_sync_apis().project_api.save_project_if_not_exists(project_name)

def load_all_project_names():
    project_names = get_sync_apis().project_api.load_all_project_names()
    return project_names