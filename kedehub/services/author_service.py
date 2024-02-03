from kedehub.gitclient.git_utility import get_name, get_email
from kedehub_client import get_sync_apis

def save_new_author(author_line):
    name = get_name(author_line)
    email = get_email(author_line)
    apis = get_sync_apis()
    author = apis.author_api.save_new_author(author_line, name, email)
    return author

def load_authors_per_project(project_name, names_to_authors):
    authors = list()
    for canonical_name in load_authors_for_projects([project_name]):
        authors.append(names_to_authors.get(canonical_name))
    return authors

def load_authors_for_projects(project_names):
    apis = get_sync_apis()
    return apis.author_api.find_all_authors_for_projects(project_names)

def build_author_map(project_name):
    apis = get_sync_apis()
    return apis.author_api.build_author_map(project_name)

def find_author_by_cannonical_name_or_aliase(name):
    apis = get_sync_apis()
    return apis.author_api.get_author_by_cannonical_name_or_aliase(name)

def assign_author_to_user_profile(author):
    apis = get_sync_apis()
    authors_updated = apis.author_api.update_author_to_user_profile(author)
    return authors_updated