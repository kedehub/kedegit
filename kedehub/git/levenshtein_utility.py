from collections import Counter
from unidiff.patch import (
    LINE_TYPE_ADDED,
    LINE_TYPE_CONTEXT,
    LINE_TYPE_REMOVED,
    Hunk,
    Line,
)
from Levenshtein import editops

MAX_LINE_LENGTH = 1000

LINE_DELETED_KEY = 'deleted'

LINE_ADDED_KEY = 'added'


def find_added_deleted_chars(removed_line: Line, added_line: Line):
    return get_levenstein_ops(cleanup_line(removed_line), cleanup_line(added_line))


def get_levenstein_ops(removed_line, added_line):
    len_removed_line = len(removed_line)
    len_added_line = len(added_line)
    if len_removed_line == 0 and len_added_line > 0:
        return Counter({LINE_ADDED_KEY : len_added_line})
    elif len_removed_line > 0 and len_added_line == 0:
        return Counter({LINE_DELETED_KEY: len_removed_line})
    elif len_removed_line == 0 and len_added_line == 0:
        return Counter()

    try:
        ops = editops(removed_line, added_line)
    except MemoryError as error:
        # Output expected MemoryErrors.
        print(error)
        return Counter({LINE_ADDED_KEY : len_added_line, LINE_DELETED_KEY: len_removed_line})
    except Exception as exception:
        # Output unexpected Exceptions.
        print(exception)
        return Counter({LINE_ADDED_KEY : len_added_line, LINE_DELETED_KEY: len_removed_line})

    ops_counter = Counter(op[0] for op in ops)
    counter = Counter()
    # In order to replace a char it needs to be added.
    # That is why we count 'replace' as added.
    counter[LINE_ADDED_KEY] = ops_counter['insert'] + ops_counter['replace']
    # In order to replace a char it needs to be deleted first.
    # That is why we count 'replace' as deleted.
    counter[LINE_DELETED_KEY] = ops_counter['delete'] + ops_counter['replace']
    return counter


def cleanup_line(line):
    '''
    Removes all righthand intervals and new lines.
    The lefthand and inbetween intervals are retained because they are valid keystrokes.
    '''
    return line.value.rstrip('\n').rstrip(' ')

def find_added_deleted_chars_in_hunk(hunk:Hunk):
    hunk_counter = Counter()
    block_removed_lines = ''
    bloack_added_lines = ''
    for line in hunk:
        if line.is_removed:
            block_removed_lines+= cleanup_line(line)[0:MAX_LINE_LENGTH]
        if line.is_added:
            bloack_added_lines+=cleanup_line(line)[0:MAX_LINE_LENGTH]
        if line.is_context:
            hunk_counter += get_levenstein_ops(block_removed_lines, bloack_added_lines)
            block_removed_lines = ''
            bloack_added_lines = ''

    if len(bloack_added_lines) > 0 or len(block_removed_lines) > 0:
        hunk_counter += get_levenstein_ops(block_removed_lines, bloack_added_lines)

    return hunk_counter


def get_removed_lines(hunk: Hunk):
    return (l for l in hunk if l.is_removed)

def get_removed_lines_as_string(hunk: Hunk):
    return ''.join([cleanup_line(l) for l in get_removed_lines(hunk)])

def get_added_lines(hunk: Hunk):
    return (l for l in hunk if l.is_added)

def get_added_lines_as_string(hunk: Hunk):
    return ''.join([cleanup_line(l) for l in get_added_lines(hunk)])