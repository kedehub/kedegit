import logging
import re

from .idmatching.filtering import is_ignored_email
from .matcher import IdentityMatcher, FilteredIdentity
from ..services.dro.user_dto import User

EMAIL_ADDRESS_REGEX = r"^(?P<email>[^\s@]+@[^\s@.]+\.[^\s@]+)$"

logger = logging.getLogger(__name__)


class EmailIdentity(FilteredIdentity):
    """Class to stored EmailName filtered identities"""

    def __init__(self, canonical_name, user_id, email):
        super(EmailIdentity, self).__init__(canonical_name, user_id)
        self.email = email

    def to_dict(self):
        return {
                'canonical_name': self.canonical_name,
                'user_id': self.user_id,
                'email': self.email
               }


class EmailMatcher(IdentityMatcher):
    """
    Simple unique identities matcher.
    This matcher only produces a positive result when two identities
    from each unique identity share the same email address. When `strict`
    is set, the email must be well-formed. It also returns a positive
    match when the uuid on both unique identities is equal.
    :param blacklist: list of entries to ignore during the matching process
    :param sources: only match the identities from these sources
    :param strict: strict matching with well-formed email addresses
    """
    def __init__(self, blacklist=None, sources=None, strict=True):
        super(EmailMatcher, self).__init__(blacklist=blacklist,
                                           sources=sources,
                                           strict=strict)
        self.email_pattern = re.compile(EMAIL_ADDRESS_REGEX)

    def match(self, a, b):
        """Determine if two unique identities are the same.
        This method compares the email addresses of each identity to check
        if the given unique identities are the same. When the given unique
        identities are the same object or share the same UUID, this will
        also produce a positive match.
        Identities which their email addresses are in the blacklist will be
        ignored and the result of the comparison will be false.
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

        for fa in filtered_a:
            for fb in filtered_b:
                if self.match_filtered_identities(fa, fb):
                    return True
        return False

    def match_filtered_identities(self, fa, fb):
        """Determine if two filtered identities are the same.
        The method compares the email addresses of each filtered identity
        to check if they are the same. When the given filtered identities
        are the same object or share the same UUID, this will also
        produce a positive match.
        Identities which their email addresses are in the blacklist will be
        ignored and the result of the comparison will be false.
        :param fa: filtered identity to match
        :param fb: filtered identity to match
        :returns: True when both filtered identities are likely to be the same.
            Otherwise, returns False.
        :raises ValueError: when any of the given filtered identities is not
            an instance of EmailIdentity class.
        """
        if not isinstance(fa, EmailIdentity):
            raise ValueError("<fa> is not an instance of EmailIdentity")
        if not isinstance(fb, EmailIdentity):
            raise ValueError("<fb> is not an instance of EmailIdentity")

        if fa.user_id and fb.user_id and fa.user_id == fb.user_id:
            return True

        if self._check_blacklist(fa):
            return False

        # Compare email addresses first
        if fa.email and fa.email == fb.email:
            return True

        return False

    def filter(self, u):
        """Filter the valid identities for this matcher.
        :param u: unique identity which stores the identities to filter
        :returns: a list of identities valid to work with this matcher.
        :raises ValueError: when the unique identity is not an instance
            of UniqueIdentity class
        """
        if not isinstance(u, User):
            raise ValueError("<u> is not an instance of User")

        filtered = []

        for author in u.identities:

            if self._check_blacklist(author):
                continue

            email = author.email.lower() if author.email else None

            if email:
                fid = EmailIdentity(author.canonical_name, author.user_id, email)
                filtered.append(fid)

        return filtered

    @staticmethod
    def matching_criteria():
        """List of keys used during the matching phase.
        returns: a list of keys
        """
        return ['email']

    def _check_blacklist(self, id_):
        if not id_.email:
            return False

        if self._check_value_in_blacklist(id_.email):
            return True

        if is_ignored_email(id_.email):
            return True

        return False

    def _check_email(self, email):
        if not email:
            return False

        checked = self.email_pattern.match(email) is not None

        return checked

    def _check_value_in_blacklist(self, value):
        return value and value.lower() in self.blacklist