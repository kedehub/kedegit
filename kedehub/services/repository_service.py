from kedehub_client import get_sync_apis
from kedehub import server_config
from kedehub.services import merge_repo_from_db_and_config
from kedehub.services.dro.repository_dto import Repository


def save_new_repo(origin, configuration_file_path, earliest_date, repository_path):
    repo = Repository( origin = origin,
                        repository_path = repository_path,
                        configuration_file_path = configuration_file_path,
                        start_time = earliest_date)
    new_repo = get_sync_apis().repository_api.save_new_repository(repo)
    new_repo.repository_path = repository_path
    new_repo.configuration_file_path = configuration_file_path
    new_repo._init_properties()
    server_config.add_new_repo(origin, repository_path, configuration_file_path)
    return new_repo


def load_reposotories_for_project(project_name):
    repositories = get_sync_apis().repository_api.load_reposotories_for_project(project_name)
    for repo in repositories:
        merge_repo_from_db_and_config(server_config.get_repos(), repo)
        if repo.repository_path is None:
            repositories.remove(repo)
        else:
            repo._init_properties()
    return repositories

def find_reposotories_for_project(project_name):
    return get_sync_apis().repository_api.load_reposotories_for_project(project_name)


def load_company_repositories():
    repositories = get_sync_apis().repository_api.get_company_repositories()
    for repo in repositories:
        merge_repo_from_db_and_config(server_config.get_repos(), repo)
        repo._init_properties()
    return repositories
