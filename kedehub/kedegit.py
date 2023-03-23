import datetime
import os
import re
from operator import itemgetter
from tqdm import tqdm
from . import server_config
from .git.git_utility import _make_diffed_commit_char_stats, EMPTY_TREE_SHA, get_git_repository, \
    get_parrent_commit, get_repository_remote_origin_url, is_commit_merged_after_a_datetime, \
    filter_invalid_unicode_sequences
from .services.author_service import save_new_author
from .services.commit_service import save_new_commit, \
    find_last_commit_for_repository, delete_commits_for_repository
from .services.dro.commit_dto import Commit
from .services.repository_service import save_new_repo, load_reposotories_for_project
from .utility.time_utility import time_to_utc_offset
from .config import Configuration
from .services.project_service import assign_new_repo_to_existing_project, ensure_project_exists

DEFAULT_CONFIGURATION_FILE_NAME = 'kede-config.json'

_diff_stat_regex = re.compile('^([0-9]+|-)\t([0-9]+|-)\t(.*)$')


def _is_commit_in_range(last_commit_for_repository: Commit, commit):
    if not last_commit_for_repository:
        return True
    else:
        # last_commit_for_repository.commit_time is in UTC timezone
        return is_commit_merged_after_a_datetime(commit, last_commit_for_repository.commit_time)

def _print_line_counts(line_counts):
    for author, count in sorted(line_counts.items(), key=itemgetter(1), reverse=True):
        print('{:>10}  {}'.format(count, author.canonical_name))


def _author_line(commit):
    return filter_invalid_unicode_sequences('{} <{}>'.format(commit.author.name, commit.author.email))


def iter_sources(repository_path, configuration_file_path=None):
    if configuration_file_path is None:
        configuration_file_path = os.path.join(repository_path, DEFAULT_CONFIGURATION_FILE_NAME)
    configuration = Configuration(configuration_file_path)
    repository = get_git_repository(repository_path)
    for git_object in repository.tree().traverse(visit_once=True):
        if git_object.type != 'blob':
            continue
        if configuration.is_source_file(git_object.path):
            yield 'source-file', git_object.path


class KedeGit:

    def _init_properties(self):
        self._repositories = []
        self._names_to_authors = {}
        self._shas_to_commits = {}

    def _is_commit_processed(self, commit_id):
        return commit_id in self._shas_to_commits

    def _add_author_if_needed(self, repository, commit):
        author_line = _author_line(commit)
        if not self._names_to_authors.get(author_line):
            try:
                author = save_new_author(author_line)
                self._names_to_authors[author_line] = author
            except Exception as e:
                print('Author: {}'.format(e))

    def _create_commit_object(self, repository, commit, author_cannonical_name):
        commit_time, commit_time_utc_offset = time_to_utc_offset(commit.authored_datetime)
        commit_object = Commit(hexsha=commit.hexsha,
                               author_name=author_cannonical_name,
                               added_lines=0,
                               added_chars=0,
                               deleted_lines=0,
                               deleted_chars=0,
                               lang_count = {},
                               commit_time=commit_time,
                               commit_time_utc_offset=commit_time_utc_offset,
                               parent_ids = [],
                               repository_id = repository.id)
        if len(commit.parents) <= 1:
            parent_commit = get_parrent_commit(commit, repository.git_repository)
            lines_added, lines_deleted, chars_aded, chars_deleted, lang_counter = _make_diffed_commit_char_stats(commit,
                                                                                                   parent_commit,
                                                                                                   repository.configuration)
            if parent_commit.hexsha != EMPTY_TREE_SHA:
                commit_object.parent_ids = parent_commit.hexsha
            commit_object.added_lines = lines_added
            commit_object.added_chars = chars_aded
            commit_object.deleted_lines = lines_deleted
            commit_object.deleted_chars = chars_deleted
            commit_object.lang_count = lang_counter

        return commit_object

    def _process_repository(self, repository):
        print('Repository {}'.format(repository.origin))
        last_commit_for_repository = find_last_commit_for_repository(repository.id)
        count_processed_committs = 0
        for commit in self._iter_unprocessed_commits(repository, last_commit_for_repository):
            self._add_author_if_needed(repository, commit)
            author_line = _author_line(commit)
            commit_object = self._create_commit_object(repository, commit, author_line)
            self._shas_to_commits[commit.hexsha] = commit_object
            repository.head_commit_id = commit.hexsha
            save_new_commit(commit_object)
            count_processed_committs +=1
        return count_processed_committs

    def _iter_branch(self, repository):
        commits = []
        commit_id = repository.head_commit_id
        while commit_id:
            commit = self._shas_to_commits.get(commit_id)
            if commit:
                commits.append(commit)
                commit_id = commit.parent_ids[0] if commit.parent_ids else None
            else:
                break
        return reversed(commits).__iter__()

    def _iter_unprocessed_commits(self, repository, last_commit_for_repository):
        # https://git-scm.com/docs/git-log
        # --all - This shows all refs in the repo, instead of only the current branch.
        # Pretend as if all the refs in refs/, along with HEAD, are listed on the command line as <commit>.
        # git log --all --reverse --date-order --format='%H'
        commits = repository.git_repository.git.log(all=True, reverse=True, date_order=True,
                                                       format='%H').splitlines()
        for commit_id in tqdm(iterable=commits, desc='Processing commits'):
            if not self._is_commit_processed(commit_id):
                commit = repository.git_repository.commit(commit_id)
                if _is_commit_in_range(last_commit_for_repository, commit):
                    yield commit

    def __init__(self, project_name):
        start_time = datetime.datetime.now()
        self.project_name = project_name
        self._init_properties()
        self._repositories = load_reposotories_for_project(self.project_name)
        print('KedeGit Init time {}'.format(datetime.datetime.now() - start_time))

    def add_repository(self, repository_path, configuration_file_path=None, **kwargs):
        count_processed_committs = 0
        new_project = ensure_project_exists(self.project_name)
        self.project_name = new_project.project_name

        repository_path = os.path.abspath(repository_path)
        if not configuration_file_path:
            configuration_file_path = os.path.join(server_config.get_config_dir(), DEFAULT_CONFIGURATION_FILE_NAME)
        else:
            configuration_file_path = os.path.abspath(configuration_file_path)
        if not next((repo for repo in self._repositories if repo.repository_path == repository_path), None):
            origin = get_repository_remote_origin_url(get_git_repository(repository_path))
            dbrepo = save_new_repo(origin, configuration_file_path, kwargs.get('earliest_date'), repository_path)
            self._repositories.append(dbrepo)
            assign_new_repo_to_existing_project(self.project_name, dbrepo.id)
            count_processed_committs = self._process_repository(dbrepo)
        return count_processed_committs

    def update_data(self):
        count_processed_committs = 0
        for repository in self._repositories:
            count_processed_committs += self._process_repository(repository)
        return count_processed_committs

    def delete_project_commits(self):
        count_deleted_committs = 0
        for repository in self._repositories:
            count_deleted_committs += delete_commits_for_repository(repository.id)
        return count_deleted_committs


