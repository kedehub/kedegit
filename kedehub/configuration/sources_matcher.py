import os
import re
import fnmatch

_double_star_after_invalid_regex = re.compile(r'[^/\\]\*\*')
_double_star_first_before_invalid_regex = re.compile('^\\*\\*[^/]')
_double_star_middle_before_invalid_regex = re.compile(r'[^\\]\*\*[^/]')


def _match_component(pattern_component, file_name_component):
    regex = fnmatch.translate(pattern_component)
    reobj = re.compile(regex)
    result = bool(reobj.match(file_name_component))
    return result


def _match_components(pattern_components, file_name_components):
    if len(pattern_components) == 0 and len(file_name_components) == 0:
        return True
    if len(pattern_components) == 0:
        return False
    if len(file_name_components) == 0:
        return len(pattern_components) == 1 and pattern_components[0] == '**'
    if pattern_components[0] == '**':
        return _match_components(pattern_components, file_name_components[1:]) or _match_components(
            pattern_components[1:], file_name_components)
    else:
        return _match_component(pattern_components[0], file_name_components[0]) and _match_components(
            pattern_components[1:], file_name_components[1:])


def match(pattern, file_name):
    """Match a glob pattern against a file name.

    Glob pattern matching is for file names, which do not need to exist as files on the file system.
    A file name is a sequence of directory names, possibly followed by the name of a file, with the
    components separated by a path separator. A glob pattern is similar, except it may contain special
    characters: A '?' matches any character in a name. A '*' matches any sequence of characters (possibly
    empty) in a name. Both of these match only within a single component, i.e., they will not match a
    path separator. A component in a pattern may also be a literal '**', which matches zero or more
    components in the complete file name. A backslash '\\' in a pattern acts as an escape character,
    and indicates that the following character is to be matched literally, even if it is a special
    character.

    :param pattern: The pattern to match. The path separator in patterns is always '/'.
    :param file_name: The file name to match against. The path separator in file names is the platform separator
    :return: True if the pattern matches, False otherwise
    """
    if _double_star_after_invalid_regex.search(pattern) is not None or _double_star_first_before_invalid_regex.search(
            pattern) is not None or _double_star_middle_before_invalid_regex.search(pattern) is not None:
        raise ValueError('** in {} not alone between path separators'.format(pattern))
    pattern = pattern.rstrip('/')
    file_name = file_name.rstrip('/')
    while '**/**' in pattern:
        pattern = pattern.replace('**/**', '**')
    pattern_components = pattern.split('/')
    file_name_components = file_name.split(os.sep)
    return _match_components(pattern_components, file_name_components)
