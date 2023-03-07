from .email import EmailMatcher
from .email_name import EmailNameMatcher

SORTINGHAT_IDENTITIES_MATCHERS = {
                                  'default': EmailMatcher,
                                  'email': EmailMatcher,
                                  'email-name': EmailNameMatcher
                                  }