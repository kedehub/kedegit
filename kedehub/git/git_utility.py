import os
import re
from collections import Counter
from datetime import datetime
import errno
from git import Repo, Commit
from unidiff import PatchSet

# https://stackoverflow.com/questions/9765453/is-gits-semi-secret-empty-tree-object-reliable-and-why-is-there-not-a-symbolic/9766506#9766506
from kedehub.git.levenshtein_utility import find_added_deleted_chars_in_hunk, LINE_DELETED_KEY, LINE_ADDED_KEY
from kedehub.language.detect_language import detect_language
from kedehub.utility.time_utility import _time_offset_to_local_time

MAX_NUMBER_OF_FILES_IN_DIFF = 199

EMPTY_TREE_SHA = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
_name_regex = re.compile('^(.*)\\s+(<.*>)$')

def _count_lines_in_a_patch(lines_added, lines_deleted, patch):
    lines_added += patch.added
    lines_deleted += patch.removed
    return lines_added, lines_deleted


def _init_patch(a_rawpath, b_rawpath, modify_diff):
    try:
        a_path = "--- " + a_rawpath.decode('utf-8')
        b_path = "+++ " + b_rawpath.decode('utf-8')
    except UnicodeDecodeError:
        a_path = "--- " + a_rawpath.decode('latin-1')
        b_path = "+++ " + b_rawpath.decode('latin-1')
    # lie to Python about the encoding, and claim that it's actually Latin-1.
    # This particular encoding has the attractive feature that every byte maps exactly
    # to its own Unicode code point, so you can read binary data as text and get away with it.
    # But then, of course, any actual UTF-8 will be converted to mojibake
    # (so "hëlló" will render as "hÃ«llÃ³" for example).
    # TODO consider usage of  https://chardet.github.io/
    try:
        return PatchSet(a_path + os.linesep + b_path + os.linesep + modify_diff.diff.decode('latin-1'))
    except:
        # print('Problem parsing this file - probably added as binary:\n'+a_path+'/'+b_path)
        return None

def log_exception(exception: BaseException, expected: bool = True):
    """Prints the passed BaseException to the console, including traceback.

    :param exception: The BaseException to output.
    :param expected: Determines if BaseException was expected.
    """
    output = "[{}] {}: {}".format('EXPECTED' if expected else 'UNEXPECTED', type(exception).__name__, exception)
    print(output)

def _make_diffed_commit_char_stats(commit, previous_commit, configuration):
    lines_added = 0
    lines_deleted = 0
    chars_aded = 0
    chars_deleted = 0
    lang_counter = Counter()
    # Generating patch text with -p
    # https://git-scm.com/docs/diff-format
    try:
        diff_index_text = previous_commit.diff(commit, create_patch=True)
    except MemoryError as error:
        # Output expected MemoryErrors.
        log_exception(error, False)
        return lines_added, lines_deleted, chars_aded, chars_deleted, dict(lang_counter)
    except Exception as exception:
        # Output unexpected Exceptions.
        log_exception(exception, False)
        return lines_added, lines_deleted, chars_aded, chars_deleted, dict(lang_counter)

    # Reason for handing only a certain number of files
    # https://github.com/microsoft/DNS-Challenge/commit/277c86839e3f154d9de00c415fd4da7ad965bf4e
    #
    # https://gitpython.readthedocs.io/en/stable/reference.html?highlight=DiffIndex#git.diff.DiffIndex
    processed_files_counter=0
    for diff in diff_index_text:
        # Filter out a small number of commits that were modifying
        # more than 1000 files each. These large commits primarily fall into two classes:
        # The majority re merge commits.
        # The rest are mostly the result of search and replace operations across a large
        # number of files—e.g. replacing http through https4
        if processed_files_counter> MAX_NUMBER_OF_FILES_IN_DIFF:
            print('The diff is too large. We only processed the first {} changed out of {} files'.format(processed_files_counter,len(diff_index_text)))
            break

        if diff.new_file:
            if not configuration.is_source_file(diff.b_path):
                continue
            patch_set = _init_patch(diff.b_rawpath, diff.b_rawpath, diff)
            if not patch_set:
                continue
        elif diff.deleted_file:
            if not configuration.is_source_file(diff.a_path):
                continue
            patch_set = _init_patch(diff.a_rawpath, diff.a_rawpath, diff)
            if not patch_set:
                continue
        elif diff.a_blob and diff.b_blob and diff.a_blob != diff.b_blob:
            if not configuration.is_source_file(diff.b_path):
                continue
            patch_set = _init_patch(diff.a_rawpath, diff.b_rawpath, diff)
            if not patch_set:
                continue
        else:
            continue

        for patch in patch_set:
            lines_added, lines_deleted = _count_lines_in_a_patch(lines_added, lines_deleted, patch)

            patch_chars_aded, patch_chars_deleted = count_added_deleted_chars_simplest_levenstein(patch)

            if(diff.b_path):
                lang_counter.update({detect_language(diff.b_path):patch_chars_aded})

            chars_aded += patch_chars_aded
            chars_deleted += patch_chars_deleted

            processed_files_counter +=1

    return lines_added,lines_deleted,chars_aded,chars_deleted, dict(lang_counter)

def count_added_deleted_chars_simplest_levenstein(patch):
    counter = Counter()
    for hunk in patch:
        counter.update(find_added_deleted_chars_in_hunk(hunk))

    return counter[LINE_ADDED_KEY], counter[LINE_DELETED_KEY]

def _commit_exists(git_repository, hexsha):
    status = 1
    try:
        status, out, err = git_repository.git.cat_file('-e', hexsha, with_extended_output=True,
                                                              with_exceptions=False)
    except OSError as error:
        print('Exception: ({}).'.format(error))
        if error.errno == errno.ENOMEM:
            git_repository.__del__()
            status, out, err = git_repository.git.cat_file('-e', hexsha, with_extended_output=True,
                                                           with_exceptions=False)
        else:
            raise error
    return status == 0


def get_git_repository(repository_path):
    try:
        repository = Repo(repository_path)
    except:
        return None
    return repository

def get_repository_remote_origin_url(repo: Repo):
    git = repo.git
    # Command to get URL for repository: (your_remote)
    # git config --get remote.origin.url
    # remoteUrl = git.config('--get', 'remote.origin.url')
    # alternative
    remoteUrl = repo.remote('origin').config_reader.get('url')
    return remoteUrl

def get_parrent_commit(commit, git_repository):
    parent_commit = []
    if len(commit.parents) == 1 and _commit_exists(git_repository, commit.parents[0]):
        parent_commit = commit.parents[0]
    else:
        parent_commit = git_repository.tree(EMPTY_TREE_SHA)
    return parent_commit

def get_email(canonical_name):
    match = _name_regex.match(canonical_name)
    if match:
        return match.group(2).rstrip('>').lstrip('<')
    else:
        return None

def get_name(canonical_name):
    match = _name_regex.match(canonical_name)
    if match:
        return match.group(1)
    else:
        return None


def get_repo_name(repo_clone_url):
    # https://stackoverflow.com/questions/55132481/retrieve-github-repository-name-using-gitpython
    repo_name = repo_clone_url.split('.git')[0].split('/')[-1]
    return repo_name


def is_commit_merged_after_a_datetime(commit: Commit, datetime_to_compare_to: datetime):
    # datetime_to_compare_to is in UTC timezone
    # commit.committer_tz_offset is in some local timezone
    # in order to compare the two datetime values they must be in the same timezone
    # that's why we make datetime_to_compare_to_in_tz to be in the timezone of commit.committer_tz_offset
    datetime_to_compare_to_in_tz = _time_offset_to_local_time(datetime_to_compare_to,
                                                                     commit.committer_tz_offset)
    # The author is who wrote the patch
    # The committer is who merged the patch
    # https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git
    # The author date notes when this commit was originally made (i.e. when you finished the git commit).
    # The commit date gets changed every time the commit is being modified, for example when merge, rebase etc.
    # https://gist.github.com/x-yuri/ec13ea740f766e72430ed8b9a9a72884#cherry-pick
    # We need to use committed_datetime because an aothor may make commits in a
    # local branch WITHOUT merging the branch to remote origin
    return commit.committed_datetime > datetime_to_compare_to_in_tz

def filter_invalid_unicode_sequences(author_line: str):
    """
        filter invalid unicode sequences before passing them to SQLAlchemy.
        See https://github.com/psycopg/psycopg2/issues/586


    :param author_line: author canonical name
    :return: author canonical name with invalid unicode sequences filtered
    """
    str_with_fixed_encoding = author_line
    try:
        str_with_fixed_encoding = author_line.encode('utf8', 'surrogateescape').decode('utf8')
    except UnicodeDecodeError:
        str_with_fixed_encoding = author_line.encode('utf8', 'surrogateescape').decode('ISO-8859-1')

    return str_with_fixed_encoding