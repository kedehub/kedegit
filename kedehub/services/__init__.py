def merge_repo_from_db_and_config(repos_data_from_config, repo_from_db):
    for repo_data_from_config in repos_data_from_config:
        if (repo_from_db.origin == repo_data_from_config['origin']):
            repo_from_db.repository_path = repo_data_from_config['repository_path']
            repo_from_db.configuration_file_path = repo_data_from_config['configuration_file_path']