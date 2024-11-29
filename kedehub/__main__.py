# based on https://github.com/pyinstaller/pyinstaller/issues/2322
import multiprocessing as mp
if __name__ == '__main__':
    mp.freeze_support()
    mp.set_start_method('spawn')

import argparse
import datetime
import os
import sys
from tqdm import tqdm
from dateutil.parser import parse

from kedehub import bcolors
from kedehub.gitclient.git_utility import get_repo_name, get_git_repository, get_repository_remote_origin_url
from kedehub.gitcloner.git_cloner import GitCloner, clone_a_repo
from kedehub.gitcloner.github_repos import GithubClient
from kedehub.gitcloner.gogs_repos import GogsClient
from kedehub.utility.os_utils import delete_folder_contents
from kedehub.gitupdater.gitupdater import update_repositories
from kedehub.kedegit import KedeGit, iter_sources
from kedehub.services.author_service import load_authors_for_projects, build_author_map
from kedehub.services.kede_service import calculate_kede_for_person, \
    calculate_weekly_kede_for_person, find_wrongly_calculated_kede_stats_for_authors_repo_id, delete_kede_for_repo
from kedehub.services.project_service import load_all_project_names
from kedehub.services.repository_service import load_company_repositories, find_reposotories_for_project
from kedehub.services.ranklist_service import calculate_rank
from kedehub.services.template_finder import manage_suspected_templates, ask_to_save_templates, \
    update_suspected_templates

from kedehub.summary import *

def make_kedegit(project):
    return KedeGit(project)

def fix_wrongly_calculated_kede(options):
    projects_to_update = options.project
    if not projects_to_update:
        projects_to_update = load_all_project_names()

    number_or_projects_to_check = len(projects_to_update)
    project_number = 1
    successful_fixes = 0

    for project in projects_to_update:
        print('Checking calculated KEDE for project: {}, #{} of {}'.format(project, project_number, number_or_projects_to_check))

        number_wrongly_calculated_kede_rows, wrong_reposotories = find_wrongly_calculated_kede_for_project(project)
        if number_wrongly_calculated_kede_rows > 0:
            print('Found wrongly calculated KEDE.')
            print('Fixing calculated KEDE...')
            delete_kede_for_repositories(wrong_reposotories)
            update_daily_kede([project],None)

            update_weekly_kede([project], None)
            number_wrongly_calculated_kede_rows, wrong_reposotories = find_wrongly_calculated_kede_for_project(project)
            if number_wrongly_calculated_kede_rows == 0:
                print(bcolors.OKGREEN, 'Successfully fixed KEDE for project {}.'.format(project), bcolors.ENDC)
                successful_fixes = successful_fixes + 1
            else:
                print(bcolors.FAIL, "Unable fo fix KEDE for project {}".format(project), bcolors.ENDC)
        else:
            print(bcolors.OKGREEN, "Everything is OK!", bcolors.ENDC)

        project_number = project_number + 1

    print('Successfully fixed {} out of {} projects.'.format(successful_fixes, number_or_projects_to_check ))


def find_wrongly_calculated_kede_for_project(project):
    number_wrongly_calculated_kede_rows = 0
    repositories = find_reposotories_for_project(project)
    wrong_reposotories = []
    for repo in tqdm(iterable=repositories, desc='Repositories:'):
        wrong_rows_for_this_repo = 0

        result = find_wrongly_calculated_kede_stats_for_authors_repo_id(repo.id, 'D')
        wrong_rows_for_this_repo += len(result.index)

        result = find_wrongly_calculated_kede_stats_for_authors_repo_id(repo.id, 'W')
        wrong_rows_for_this_repo += len(result.index)

        if wrong_rows_for_this_repo > 0:
            wrong_reposotories.append(repo)
            number_wrongly_calculated_kede_rows +=wrong_rows_for_this_repo
    return number_wrongly_calculated_kede_rows, wrong_reposotories

def delete_kede_for_repositories(repositories):
    for repo in tqdm(iterable=repositories, desc='Deleting KEDE for repositories:'):
        delete_kede_for_repo(repo.id)

def update_project(options):
    projects_to_update = options.project
    if not projects_to_update:
        projects_to_update = load_all_project_names()

    number_or_projects_to_update = len(projects_to_update)
    project_number = 1
    successful_updates = 0
    for project in projects_to_update:
        print('Updating Kedehub for project: {}, #{} of {}'.format(project, project_number, number_or_projects_to_update))
        kedegit = make_kedegit(project)

        # clone all origins
        if options.temp:
            for repository in kedegit._repositories:
                delete_folder_contents(repository.repository_path)
                clone_a_repo(repository.repository_path, repository.origin)

        if options.clean:
            count_deleted_commits = kedegit.delete_project_commits()
            print('Deleted #{} commits for project: {}'.format(count_deleted_commits, project))

        count_processed_committs = kedegit.update_data()
        if (count_processed_committs > 0):
            calculate_stats_for_authors(kedegit.project_name, kedegit._names_to_authors.keys())
            successful_updates = successful_updates + 1
        project_number = project_number + 1

        # empty repo folders
        if options.temp:
            for repository in kedegit._repositories:
                delete_folder_contents(repository.repository_path)

    print('Successfully updated {} out of {} projects'.format(successful_updates, number_or_projects_to_update))

def update_repos(options):
    repositories = load_company_repositories()
    update_repositories(repositories)

def add_repository_to_a_project(options):
    if options.project is None:
        return

    count_processed_committs, project_name = _add_repository(options.project, options.repository, options.configuration, options.earliest_commit_date)

    if ((count_processed_committs > 0)):
        calculate_stats_for_project(project_name)

    print('Successfully initialized project with ID = {} '.format(project_name))
    return count_processed_committs, project_name

def _add_repository(project, repository, configuration = None, earliest_commit_date = None):
    print('Adding repo: {} to project {}'.format(repository, project))
    kedegit = make_kedegit(project)
    count_processed_committs = 0
    if earliest_commit_date:
        date = parse(earliest_commit_date)
        if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
            date = date.replace(tzinfo=datetime.timezone.utc)
        count_processed_committs = kedegit.add_repository(repository, configuration, earliest_date=date)
    else:
        count_processed_committs = kedegit.add_repository(repository, configuration)
    return count_processed_committs, kedegit.project_name

def list_projects(_):
    for name in load_all_project_names():
        print(name)


def list_sources(options):
    for item_type, item in iter_sources(options.repository, options.configuration):
        if item_type == 'source-file':
            print('S: {}'.format(item))

def calculate_ranklist(options):
    if options.type == 'calculate':
        calculate_rank(options.last_week,
                           options.today)

def calculate_stats(options):
    authors_to_update = options.author
    projects_to_update = options.project
    if not projects_to_update:
        projects_to_update = load_all_project_names()
    if options.type == 'calculate-kede':
        update_daily_kede(projects_to_update, authors_to_update)
    elif options.type == 'calculate-weekly-kede':
        update_weekly_kede(projects_to_update, authors_to_update)


def update_weekly_kede(projects_to_update, authors_to_update):
    number_or_projects_to_update = len(projects_to_update)
    project_number = 1
    for project in projects_to_update:
        print('Updating weekly KEDE for project: {}, #{} of {}'.format(project, project_number,
                                                                       number_or_projects_to_update))
        persons = get_people_to_report_on([project], authors_to_update)
        calculate_weekly_kede_for_persons(project, persons)
        project_number = project_number + 1


def update_daily_kede(projects_to_update, authors_to_update):
    number_or_projects_to_update = len(projects_to_update)
    project_number = 1
    for project in projects_to_update:
        print('Updating Daily KEDE for project: {}, #{} of {}'.format(project, project_number,
                                                                      number_or_projects_to_update))
        persons = get_people_to_report_on([project], authors_to_update)
        calculate_daily_kede_for_persons(project, persons)
        project_number = project_number + 1


def print_summary(options):
    handle = open(options.output_file, 'w') if options.output_file else sys.stdout
    handle.write(str(commit_count_table(options.project)))

    handle.write('\n')
    if handle is not sys.stdout:
        handle.close()

def do_templates(options):
    persons = get_people_to_report_on(options.project, options.author)
    if options.type == 'find':
        for current_person in persons:
            template_commits_df = manage_suspected_templates(current_person)
            ask_to_save_templates(template_commits_df, current_person)
    elif options.type == 'update':
        update_templates_for_persons(persons)


def update_templates_for_persons(persons):
    for current_person in tqdm(iterable=persons, desc="Updating templates for persons"):
        update_suspected_templates(current_person)

def calculate_daily_kede_for_persons(project, persons):
    for current_person in tqdm(iterable=persons, desc="Calculating Daily KEDE for persons"):
        calculate_kede_for_person(project, current_person)

def calculate_weekly_kede_for_persons(project, persons):
    for current_person in tqdm(iterable=persons, desc="Calculating Weekly KEDE for persons"):
        calculate_weekly_kede_for_person(project, current_person)

def get_people_to_report_on(projects_to_show, people_to_show):
    if people_to_show:
        return people_to_show
    else:
        if projects_to_show:
            return load_authors_for_projects(projects_to_show)
        else:
            # find all projects for the company
            projects_to_update = load_all_project_names()
            available_people = []
            for current_project in projects_to_update:
                available_people.extend(load_authors_for_projects([current_project]))
            return available_people

def bulk_import_github_reps(options):
    working_directory = os.path.abspath(options.workdir)
    client = GithubClient(options.token,options.org)
    cloner = GitCloner(working_directory, client)

    try:
        repo_clone_urls = cloner.load_repos()
    except Exception as e:
        print('FATAL: Could not get repos clone URLs: ({}). Terminating.'.format(e))
        sys.exit(1)

    _bulk_import_reps(cloner, repo_clone_urls, options.project, options.temp)

def bulk_import_gogs_reps(options):
    working_directory = os.path.abspath(options.workdir)
    client = GogsClient(options.host, options.token, options.username)
    cloner = GitCloner(working_directory, client)

    try:
        repo_clone_urls = cloner.load_repos()
    except Exception as e:
        print('FATAL: Could not get repos clone URLs: ({}). Terminating.'.format(e))
        sys.exit(1)

    _bulk_import_reps(cloner, repo_clone_urls, options.project, options.temp)

def _bulk_import_reps(cloner, repo_clone_urls, project, temp: bool = False):
    number_or_repo_clone_urls = len(repo_clone_urls)
    repo_number = 1
    success_import = 0
    for repo_clone_url in repo_clone_urls:
        # Folder name should be the repo_clone_url's name
        print('Importing repo {} of {}'.format(repo_number, number_or_repo_clone_urls))

        clone_path = cloner.clone_repo(repo_clone_url)
        if project is None:
            project_name = get_repo_name(repo_clone_url)
        else:
            project_name = project

        if (clone_path):
            count_processed_committs, project_name = _add_repository(project_name, clone_path)
            if temp:
                delete_folder_contents(clone_path)
            if ((count_processed_committs > 0) and
                    (project is None)):
                calculate_stats_for_project(project_name)
            success_import = success_import + 1
        repo_number = repo_number + 1
    if project is not None:
        calculate_stats_for_project(project_name)
    print('Successfully imported {} out of {} repos'.format(success_import, number_or_repo_clone_urls))

def bulk_import_gitlab_server_reps():
    pass

def bulk_import_repos_bitbucket_cloud():
    pass

def import_gogs_repo(options):
    working_directory = os.path.abspath(options.workdir)
    client = GogsClient(options.host, options.token, options.username)
    cloner = GitCloner(working_directory, client)
    # http://git.elando.bg:3000/eLando/allianz_quotation_db.git
    repo_clone_url = options.host +'/'+ options.url

    import_repo_update_stats(cloner, repo_clone_url, options.temp)

def import_github_repo(options):
    working_directory = os.path.abspath(options.workdir)
    client = GithubClient(options.token, options.org)
    cloner = GitCloner(working_directory, client)
    # http://git.elando.bg:3000/eLando/allianz_quotation_db.git
    repo_clone_url = options.url

    import_repo_update_stats(cloner, repo_clone_url, options.temp)


def clone_github_repo(options):
    working_directory = os.path.abspath(options.workdir)
    client = GithubClient(options.token, options.org)
    cloner = GitCloner(working_directory, client)
    # http://git.elando.bg:3000/eLando/allianz_quotation_db.git
    repo_clone_url = options.url

    if repo_clone_url:
        # Folder name should be the repo_clone_url's name
        print('Importing repo {}'.format(repo_clone_url))

        clone_path = cloner.clone_repo(repo_clone_url)

    print('Successfully cloned {}'.format(repo_clone_url))

def import_repo_update_stats(cloner, repo_clone_url, temp :bool = False):
    if repo_clone_url:
        # Folder name should be the repo_clone_url's name
        print('Importing repo {}'.format(repo_clone_url))

        clone_path = cloner.clone_repo(repo_clone_url)
        project_name = get_repo_name(repo_clone_url)
        if (clone_path):
            count_processed_committs, project_name = _add_repository(project_name, clone_path)
            if temp:
                delete_folder_contents(clone_path)
            if (count_processed_committs > 0):
                calculate_stats_for_project(project_name)

    print('Successfully imported {}'.format(repo_clone_url))


def recalculate_rank_for_all_people():
    # we need to recalculate Rank for all of the KEDEhub.com
    last_week_with_rank_calculated = datetime.date(1990, 1, 1).strftime('%Y-%m-%d')
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    calculate_rank(last_week_with_rank_calculated, today)


def bulk_add_repos_from_dir(options):
    working_directory = os.path.abspath(options.workdir)
    if options.project is None:
        project = None
    else:
        project = options.project

    try:
        repo_dirs = [f.path for f in os.scandir(working_directory) if f.is_dir()]
        print('Repos to add: {}'.format(', '.join(repo_dirs)))
    except Exception as e:
        print('FATAL: Could not get sub-directories: ({}). Terminating.'.format(e))
        sys.exit(1)

    number_or_repo_dirs = len(repo_dirs)
    repo_number = 1
    success_import = 0
    project_names = set()

    for repo_dir in repo_dirs:
        # Folder name should be the repo_dir's name
        print('Importing repo {} of {}'.format(repo_number, number_or_repo_dirs))

        brepo = get_git_repository(repo_dir)
        if brepo is None:
            repo_number = repo_number + 1
            continue

        try:
            remote_origin_url = get_repository_remote_origin_url(brepo)
        except ValueError:
            print("'origin' remote does not exist for repository {}".format(brepo.git_dir))
            repo_number = repo_number + 1
            continue

        if project is None:
            project_name = get_repo_name(remote_origin_url)
        else:
            project_name = project

        project_names.add(project_name)
        print('Importing repo {} with project name {}'.format(remote_origin_url, project_name))
        count_processed_committs, project_name = _add_repository(project_name, repo_dir)
        if (count_processed_committs > 0):
            calculate_stats_for_project(project_name)
        success_import = success_import + 1
        repo_number = repo_number + 1

    print('Successfully imported {} out of {} repos'.format(success_import, number_or_repo_dirs))

    return success_import, number_or_repo_dirs, project_names

def calculate_stats_for_project(project_name):
    persons = get_people_to_report_on([project_name],None)
    update_templates_for_persons(persons)
    calculate_daily_kede_for_persons(project_name,persons)
    calculate_weekly_kede_for_persons(project_name,persons)

def calculate_stats_for_authors(project_name: str, persons):
    update_templates_for_persons(persons)
    calculate_daily_kede_for_persons(project_name,persons)
    calculate_weekly_kede_for_persons(project_name,persons)


def parse_args(args):
    parser = argparse.ArgumentParser(prog='kedehub',
                                 description='Extract KEDE statistics from Git repositories')
    command_parsers = parser.add_subparsers(dest='subparser_name')

    init_parser = command_parsers.add_parser('init-project', help='Create a new project and import one local repo to it')
    init_parser.add_argument('project', help='Name of the project to create')
    init_parser.add_argument('repository', help='Path to the local Git repository to import from')
    init_parser.add_argument('-c', '--configuration', help='Path to the repository configuration file')
    init_parser.add_argument('--earliest-commit-date', help='Ignore commits prior to this date')
    init_parser.set_defaults(func=add_repository_to_a_project)

    update_parser = command_parsers.add_parser('update-projects', help='Import all new commits from all repos of existing projects')
    update_parser.add_argument('-p','--project',nargs='+', help='Name of the project to update')
    update_parser.add_argument('--temp', dest='temp', action='store_true')
    update_parser.add_argument('--no-temp', dest='temp', action='store_false')
    update_parser.add_argument('--clean', dest='clean', action='store_true')
    update_parser.add_argument('--no-clean', dest='clean', action='store_false')
    update_parser.set_defaults(temp=False)
    update_parser.set_defaults(clean=False)
    update_parser.set_defaults(func=update_project)

    update_repos_parser = command_parsers.add_parser('update-repos', help='Update from remote all existing local repos')
    update_repos_parser.set_defaults(func=update_repos)

    add_parser = command_parsers.add_parser('add-repository', help='Import a new local repository to an existing project')
    add_parser.add_argument('project', help='Project to add the repository to')
    add_parser.add_argument('repository', help='Path to the local Git repository to import from')
    add_parser.add_argument('-c', '--configuration', help='Path to the repository configuration file')
    add_parser.add_argument('--earliest-commit-date', help='Ignore commits prior to this date')
    add_parser.set_defaults(func=add_repository_to_a_project)

    project_list_parser = command_parsers.add_parser('list-projects', help='List names of existing projects')
    project_list_parser.set_defaults(func=list_projects)

    source_list_parser = command_parsers.add_parser('list-sources', help='List source files and test lines in repository')
    source_list_parser.add_argument('repository', help='Git repository to examine')
    source_list_parser.add_argument('-c', '--configuration', help='Path to the repository configuration file')
    source_list_parser.set_defaults(func=list_sources)

    create_stats_parser(command_parsers)
    create_ranklist_parser(command_parsers)
    create_bulk_add_repos_from_dir_parser(command_parsers)
    create_templates_parser(command_parsers)

    summary_parser = command_parsers.add_parser('summary',
                                                help='Print summary information of the current state of the project')
    summary_parser.add_argument('project', help='Name of the project to summarize')
    summary_parser.add_argument('-o', '--output-file',
                                help='Name of the file to print the summary to. If omitted, summary is printed to standard output')
    summary_parser.set_defaults(func=print_summary)

    bulk_import_github_parser = command_parsers.add_parser('clone-import-github', help='Clone and import Github repos to project Default')
    bulk_import_github_parser.add_argument('--workdir', help='Path to the directory where to clone the repos')
    bulk_import_github_parser.add_argument('--org', help='GitHub org name')
    bulk_import_github_parser.add_argument('--token', help='Personal access token')
    bulk_import_github_parser.add_argument('--temp', dest='temp', action='store_true')
    bulk_import_github_parser.add_argument('--no-temp', dest='temp', action='store_false')
    bulk_import_github_parser.add_argument('-p','--project', help='Project name to be set to all repos from the org')
    bulk_import_github_parser.set_defaults(temp=False)
    bulk_import_github_parser.set_defaults(func=bulk_import_github_reps)

    import_github_parser = command_parsers.add_parser('clone-import-github-repo', help='Clone and import Github repo to project Default')
    import_github_parser.add_argument('--workdir', help='Path to the directory where to clone the repo')
    import_github_parser.add_argument('--url', help='Clone URL')
    import_github_parser.add_argument('--org', help='GitHub org name')
    import_github_parser.add_argument('--token', help='Personal access token')
    import_github_parser.add_argument('--temp', dest='temp', action='store_true')
    import_github_parser.add_argument('--no-temp', dest='temp', action='store_false')
    import_github_parser.set_defaults(temp=False)
    import_github_parser.set_defaults(func=import_github_repo)

    import_github_parser = command_parsers.add_parser('clone-github-repo', help='Clone a Github repo to project Default')
    import_github_parser.add_argument('--workdir', help='Path to the directory where to clone the repo')
    import_github_parser.add_argument('--url', help='Clone URL')
    import_github_parser.add_argument('--org', help='GitHub org name')
    import_github_parser.add_argument('--token', help='Personal access token')
    import_github_parser.add_argument('--temp', dest='temp', action='store_true')
    import_github_parser.add_argument('--no-temp', dest='temp', action='store_false')
    import_github_parser.set_defaults(temp=False)
    import_github_parser.set_defaults(func=clone_github_repo)

    bulk_import_gogs_parser = command_parsers.add_parser('clone-import-gogs', help='Clone and import Gogs repos to project Default')
    bulk_import_gogs_parser.add_argument('--workdir', help='Path to the directory where to clone the repos')
    bulk_import_gogs_parser.add_argument('--host', help='Gogs server host')
    bulk_import_gogs_parser.add_argument('--username', help='Username')
    bulk_import_gogs_parser.add_argument('--token', help='Personal access token')
    bulk_import_gogs_parser.add_argument('--temp', dest='temp', action='store_true')
    bulk_import_gogs_parser.add_argument('--no-temp', dest='temp', action='store_false')
    bulk_import_gogs_parser.add_argument('-p','--project', help='Project name to be set to all repos from the org')
    bulk_import_gogs_parser.set_defaults(temp=False)
    bulk_import_gogs_parser.set_defaults(func=bulk_import_gogs_reps)

    import_gogs_parser = command_parsers.add_parser('clone-import-gogs-repo', help='Clone and import one Gogs repo to project Default')
    import_gogs_parser.add_argument('--workdir', help='Path to the directory where to clone the repo')
    import_gogs_parser.add_argument('--url', help='Clone URL')
    import_gogs_parser.add_argument('--host', help='Gogs server host')
    import_gogs_parser.add_argument('--username', help='Username')
    import_gogs_parser.add_argument('--token', help='Personal access token')
    import_gogs_parser.add_argument('--temp', dest='temp', action='store_true')
    import_gogs_parser.add_argument('--no-temp', dest='temp', action='store_false')
    import_gogs_parser.set_defaults(temp=False)
    import_gogs_parser.set_defaults(func=import_gogs_repo)

    bulk_import_gitlab_server_parser = command_parsers.add_parser('clone-import-gitlab-server', help='Clone and import Gitlab-server repos to project Default')
    bulk_import_gitlab_server_parser.add_argument('--workdir', help='Path to the directory where to clone the repos')
    bulk_import_gitlab_server_parser.add_argument('--host', help='Gitlab-server host')
    bulk_import_gitlab_server_parser.add_argument('--token', help='Personal access token')
    bulk_import_gitlab_server_parser.set_defaults(func=bulk_import_gitlab_server_reps)

    bulk_import_bitbucket_cloud_parser = command_parsers.add_parser('clone-import-bitbucket-cloud', help='Clone and import Bitbucket-cloud repos to project Default')
    bulk_import_bitbucket_cloud_parser.add_argument('--workdir', help='Path to the directory where to clone the repos')
    bulk_import_bitbucket_cloud_parser.add_argument('--workspaceid', help='Server workspace id')
    bulk_import_bitbucket_cloud_parser.add_argument('--username', help='Username')
    bulk_import_bitbucket_cloud_parser.add_argument('--pwd', help='Password')
    bulk_import_bitbucket_cloud_parser.set_defaults(func=bulk_import_repos_bitbucket_cloud)

    create_fix_wrongly_calculated_kede_stats(command_parsers)

    return parser.parse_args(args)


def create_fix_wrongly_calculated_kede_stats(command_parsers):
    identity_merge_parser = command_parsers.add_parser('fix-kede', help='Fix if there are wrongly calculated KEDE')
    identity_merge_parser.add_argument('-p', '--project', nargs='+',
                                       help='Name of the project which KEDE to fix')
    identity_merge_parser.set_defaults(func=fix_wrongly_calculated_kede)

def create_bulk_add_repos_from_dir_parser(command_parsers):
    bulk_init_parser = command_parsers.add_parser('bulk-import-repos', help='Bulk insert into Kedehub all reps from a directory')
    bulk_init_parser.add_argument('--workdir', help='Path to the directory where are the repos')
    bulk_init_parser.add_argument('-p','--project', help='Project name to be set to all repos from the dir')
    bulk_init_parser.set_defaults(func=bulk_add_repos_from_dir)

def create_stats_parser(command_parsers):
    stats_parser = command_parsers.add_parser('stats', help='Calculates kede statistics')
    stats_parser.add_argument('type', help='The type of stats to make',
                              choices=['calculate-kede',
                                       'calculate-weekly-kede'])
    stats_parser.add_argument('-p','--project', nargs='+', help='Name of the project to caclulate')
    stats_parser.add_argument('-a', '--author', nargs='*', help='Zero, one or more author names to analyze')
    stats_parser.set_defaults(func=calculate_stats)

def create_ranklist_parser(command_parsers):
    ranklist_parser = command_parsers.add_parser('ranklist', help='Calculates rank list')
    ranklist_parser.add_argument('type', help='The type of stats to make',
                              choices=['calculate'])
    ranklist_parser.add_argument('-lw','--last_week', help='Monday date of the week to caclulate from')
    ranklist_parser.add_argument('-td','--today', help='Date from the week after the week to caclulate to')
    ranklist_parser.set_defaults(func=calculate_ranklist)

def create_templates_parser(command_parsers):
    epilog = """
         The types of action to take are:
           find - interactive mode,
           update - updates templates without asking the user
        """
    templates_parser = command_parsers.add_parser('templates',
                                                  help='Finds templates committed',
                                                  epilog=epilog)
    templates_parser.add_argument('type', help='The type of action to take',
                                  choices=['find',
                                           'update'])
    templates_parser.add_argument('-o', '--output-file',
                                  help='Name of the file to save the graph to. If omitted, graph is displayed on screen')
    templates_parser.add_argument('-p','--project', nargs='+', help='At least one name of a project to analyze')
    templates_parser.add_argument('-a','--author', nargs='*', help='Zero, one or more author names to analyze')
    templates_parser.add_argument('-r','--reporting_interval', nargs='?', default='q',
                                  choices=['y', 'q', 'm', 'w', 'd'], help='One reporting interval. Default is quarterly: q')
    templates_parser.set_defaults(func=do_templates)


def Main() -> None:
    # parse the args
    parsed_args = parse_args(sys.argv[1:])
    # Check if 'func' attribute exists
    if hasattr(parsed_args, 'func'):
        # call whatever function was selected
        parsed_args.func(parsed_args)
    else:
        print("Please provide valid arguments. Use --help for more information.")

if __name__ == '__main__':
  Main()