import logging
import re

from names_matcher import NamesMatcher

from .idmatching.filtering import is_popular_name, is_blacklisted_name, is_blacklisted_email, is_ignored_email, \
    is_ignored_name
from .matcher import IdentityMatcher, FilteredIdentity
from ..services.dro.user_dto import User

from ..utility.list_utility import list_names_and_emails

EMAIL_ADDRESS_REGEX = r"^(?P<email>[^\s@]+@[^\s@.]+\.[^\s@]+)$"
NAME_REGEX = r"^\w+\s\w+"

logger = logging.getLogger(__name__)


class EmailNameIdentity(FilteredIdentity):
    """Class to stored EmailName filtered identities"""

    def __init__(self, canonical_name, user_id, email, name):
        super(EmailNameIdentity, self).__init__(canonical_name, user_id)
        self.email = email
        self.name = name

    def to_dict(self):
        return {
                'canonical_name': self.canonical_name,
                'user_id': self.user_id,
                'email': self.email,
                'name': self.name
               }


class EmailNameMatcher(IdentityMatcher):
    """
    Complex unique identities matcher.
    This matcher produces a positive result when one of these cases
    is true (this means OR condition) on a pair of identities:
       - the UUID on both identities is equal
       - identities share the same email address
       - name field is composed by "firstname lastname" and both are
         equal; i.e: "John Smith" and "J Smith Rae" are valid name fields;
         "jonhsmith" are "j.smith" not valid. This rigorous validation is
         only done when `strict` mode is set to `True`.
    :param blacklist: list of entries to ignore during the matching process
    :param sources: only match the identities from these sources
    :param strict: strict matching with well-formed email addresses and names
    :param confidence_level: How confident shall we be in order to match two identities? Range from 0 to 1.
    """
    def __init__(self, blacklist=None, sources=None, strict=True, confidence_level = 0.99):
        super(EmailNameMatcher, self).__init__(blacklist=blacklist,
                                               sources=sources,
                                               strict=strict)
        self.email_pattern = re.compile(EMAIL_ADDRESS_REGEX)
        self.name_pattern = re.compile(NAME_REGEX)
        self.confidence_level = confidence_level

    def match(self, a, b):
        """Determine if two unique identities are the same.
        This method compares the email addresses or the names of each
        identity to check if the given unique identities are the same.
        When the given unique identities are the same object or share
        the same UUID, this will also produce a positive match.
        Identities which their email addresses or names are in the blacklist
        will be ignored during the matching.
        :param a: unique identity to match
        :param b: unique identity to match
        :returns: True when both unique identities are likely to be the same.
            Otherwise, returns False.
        :raises ValueError: when any of the given unique identities is not
            an instance of UniqueIdentity class
        """
        if not isinstance(a, User):
            raise ValueError("<a> is not an instance of User")
        if not isinstance(b, User):
            raise ValueError("<b> is not an instance of User")

        if a.id and b.id and a.id == b.id:
            return True

        filtered_a = self.filter(a)
        filtered_b = self.filter(b)

        return self.match_filtered_identities(filtered_a,filtered_b)

    def match_filtered_identities(self, fa, fb):
        """Determine if two filtered identities are the same.
        The method compares the email addresses or the names of each
        filtered identity to check if they are the same. When the given
        filtered identities are the same object or share the same UUID,
        this will also produce a positive match.
        Identities which their email addresses or names are in the blacklist
        will be ignored and the result of the comparison will be false.
        :param fa: filtered identity to match
        :param fb: filtered identity to match
        :returns: True when both filtered identities are likely to be the same.
            Otherwise, returns False.
        :raises ValueError: when any of the given filtered identities is not
            an instance of Identity class.
        """
        names_and_emails_1 = [list_names_and_emails(fa)]
        names_and_emails_2 = [list_names_and_emails(fb)]

        if (names_and_emails_1 == [[None]] * len(names_and_emails_1)) or (
                names_and_emails_2 == [[None]] * len(names_and_emails_2)):
            return False

        assignments = NamesMatcher(self.blacklist)(names_and_emails_1,
                                                   names_and_emails_2)

        confidence = assignments[1][0]

        if confidence > self.confidence_level:
            return True
        else:
            return False

    def filter(self, user):
        """Filter the valid identities for this matcher.
        :param u: unique identity which stores the identities to filter
        :returns: a list of identities valid to work with this matcher.
        :raises ValueError: when the unique identity is not an instance
            of UniqueIdentity class
        """
        if not isinstance(user, User):
            raise ValueError("<user> is not an instance of User")

        filtered = []

        for author in user.identities:

            if self._check_blacklist(author):
                continue

            if is_popular_name(author.name):
                continue

            filtered.append(author)

        return filtered

    @staticmethod
    def matching_criteria():
        """List of keys used during the matching phase.
        returns: a list of keys
        """
        return ['email', 'name']

    def _check_pattern(self, pattern, value):
        if not value:
            return False
        return pattern.match(value) is not None

    def _check_blacklist(self, id_):
        if self._check_value_in_blacklist(id_.email):
            return True
        if self._check_value_in_blacklist(id_.name):
            return True

        if is_ignored_email(id_.email):
            return True
        if is_ignored_name(id_.name):
            return True
        return False

    def _check_value_in_blacklist(self, value):
        return value and value.lower() in self.blacklist