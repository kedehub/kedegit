import logging

from tqdm import tqdm

from .exceptions import MatcherNotSupportedError


logger = logging.getLogger(__name__)


class IdentityMatcher(object):
    """Abstract class to determine whether two unique identities match.
    The object receives a list of keyword arguments. The allowed
    keys are listed below (other keywords will be ignored):
       - 'blacklist' : list of entries to ignore during the matching process
       - 'sources' : only match the identities from these sources
       - 'strict' : strict matching (i.e, well-formed email addresses);
          `True` by default
    """
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        blacklist = self._kwargs.get('blacklist', None)
        sources = self._kwargs.get('sources', None)

        if blacklist:
            self.blacklist = [entry.excluded.lower()
                              for entry in blacklist]
            self.blacklist.sort()
        else:
            self.blacklist = []

        if sources:
            self.sources = [source.lower() for source in sources]
            self.sources.sort()
        else:
            self.sources = None

        self.strict = self._kwargs.get('strict', True)

    def match(self, a, b):
        """Abstract method used to determine if both unique identities are the same.
        Take into account that some identities cannot match when this class
        was initialized with a blacklist.
        :param a: unique identity to match
        :param b: unique identity to match
        :returns: True when both unique identities are likely to be the same.
        """
        raise NotImplementedError

    def match_filtered_identities(self, fa, fb):
        """Abstract method used to determine if both filtered identities are the same.
        :param fa: filtered identity to match
        :param fb: filtered identity to match
        Take into account that some identities cannot match when this class
        was initialized with a blacklist.
        :returns: True when both filtered identities are likely to be the same.
        """
        raise NotImplementedError

    def filter(self, u):
        """Filter the valid identities for this matcher.
        Some identities can be filtered if this class was initialized
        with a blacklist.
        :param u: unique identity which stores the identities to filter
        :returns: a list of identities valid to work with this matcher.
        """
        raise NotImplementedError

    @staticmethod
    def matching_criteria():
        """List of keys used during the matching phase.
        This list is only required for matching using the fast mode
        algorithm. Otherwise, raises a `NotImplemetedError` exception.
        returns: a list of keys
        """
        raise NotImplementedError


class FilteredIdentity(object):
    """Generic class to store filtered identities"""

    def __init__(self, canonical_name, user_id):
        self.canonical_name = canonical_name
        self.user_id = user_id

    def to_dict(self):
        return {
                'canonical_name': self.canonical_name,
                'user_id': self.user_id
               }


def create_identity_matcher(matcher='default', blacklist=None, sources=None,
                            strict=True):
    """Create an identity matcher of the given type.
    Factory function that creates an identity matcher object of the type
    defined on 'matcher' parameter. A blacklist can also be added to
    ignore those values while matching.
    :param matcher: type of the matcher
    :param blacklist: list of entries to ignore while matching
    :param sources: only match the identities from these sources
    :param strict: strict matching (i.e, well-formed email addresses)
    :returns: a identity matcher object of the given type
    :raises MatcherNotSupportedError: when the given matcher type is not
        supported or available
    """
    import kedehub.matching as matching

    if matcher not in matching.SORTINGHAT_IDENTITIES_MATCHERS:
        raise MatcherNotSupportedError(matcher=str(matcher))

    klass = matching.SORTINGHAT_IDENTITIES_MATCHERS[matcher]

    return klass(blacklist=blacklist, sources=sources, strict=strict)


def match(users, matcher):
    """Find matches in a set of unique identities.
    This function looks for possible similar or equal identities from a set
    of unique identities. The result will be a list of subsets where each
    subset is a list of matching identities.
    When `fastmode` is set a new and experimental matching algorithm
    will be used. It consumes more resources (a big amount of memory)
    but it is, at least, two orders of maginute faster than the
    classic algorithm.
    :param users: list of unique identities to match
    :param matcher: instance of the matcher
    :returns: a list of subsets with the matched unique identities
    :raises MatcherNotSupportedError: when matcher does not support fast
        mode matching
    :raises TypeError: when matcher is not an instance of
        IdentityMatcher class
    """
    if not isinstance(matcher, IdentityMatcher):
        raise TypeError("matcher is not an instance of IdentityMatcher")

    filtered, no_filtered, uuids = \
        _filter_unique_identities(users, matcher)

    matched = _match(filtered, matcher)

    matched = _build_matches(matched, uuids, no_filtered)

    return matched

def match_filtered_identities(x, ids, matcher):
    """Check if an identity matches a set of identities"""

    for y in ids:
        if x.user_id == y.user_id:
            return True
        if matcher.match_filtered_identities(x, y):
            return True
    return False

def _match(filtered, matcher):
    """Old method to find matches in a set of filtered identities."""

    # Find subsets of matches
    matched = []

    pbar = tqdm(total=len(filtered) + 1, desc=('Matching by: '+type(matcher).__name__))
    while filtered:
        candidates = []
        no_match = []

        author = filtered.pop(0)

        while matched:
            ids = matched.pop(0)

            if match_filtered_identities(author, ids, matcher):
                candidates.extend(ids)
            else:
                no_match.append(ids)

        candidates.append(author)

        # Generate the new list of matched subsets
        matched = [candidates] + no_match

        pbar.update(1)

    pbar.close()

    return matched


def _filter_unique_identities(users, matcher):
    """Filter a set of unique identities.
    This function will use the `matcher` to generate a list
    of `FilteredIdentity` objects. It will return a tuple
    with the list of filtered objects, the unique identities
    not filtered and a table mapping uuids with unique
    identities.
    """
    filtered = []
    no_filtered = []
    uuids = {}

    for user in users:
        n = len(filtered)
        filtered += matcher.filter(user)

        if len(filtered) > n:
            uuids[user.id] = user
        else:
            no_filtered.append([user])

    return filtered, no_filtered, uuids


def _build_matches(matches, uuids, no_filtered):
    """Build a list with matching subsets"""

    result = []

    for m in matches:
        mk = m[0].user_id
        subset = [uuids[mk]]

        for id_ in m[1:]:
            uk = id_.user_id
            user = uuids[uk]

            if user not in subset:
                subset.append(user)

        result.append(subset)

    result += no_filtered
    result.sort(key=len, reverse=True)

    sresult = []
    for r in result:
        r.sort(key=lambda id_: id_.name)
        sresult.append(r)

    return sresult