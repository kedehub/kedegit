import itertools


def list_names(identities):
    return [x.name for x in identities]


def list_names_and_emails(identities):
    if not isinstance(identities, list):
        identities = [identities]

    return itertools.chain.from_iterable([[x.name, x.email.split("@")[0]] for x in identities])