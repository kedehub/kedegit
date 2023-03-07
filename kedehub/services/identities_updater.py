import itertools
from typing import List
from tqdm import tqdm
from pydantic import EmailStr
from kedehub.matching import EmailMatcher, EmailNameMatcher
from kedehub.matching.idmatching.filtering import is_ignored_email, is_ignored_name
from kedehub.matching.matcher import match
from kedehub.services.author_service import build_author_map, assign_author_to_user_profile
from kedehub.services.dro.user_dto import User
from kedehub.services.user_service import create_new_user
from pydantic.errors import EmailError
from kedehub.utility.input_utility import get_bool_input, auto_confirmation
from kedehub.utility.email_utility import generate_no_reply_user_email_address

def load_authors_for_project(projects_to_update: List[str]):
    authors = dict()
    for project in projects_to_update:
        authors.update(build_author_map(project))
    return authors

def identity_merge_users(project, verbose: bool = False):
        authors = load_authors_for_project(project)

        len_matched_users_by_email, \
        len_matched_users_by_email_and_name, \
        len_users, \
        len_authors, \
        matched_users_by_email_and_name, \
        users_merged_count, \
        authors_merged_count = identify_authors_to_merge(authors)

        authors_updated, users_inserted = save_identified_merged_users(matched_users_by_email_and_name)
        if verbose:
            print(matched_users_by_email_and_name)

        return len_users, \
               len_authors, \
               len_matched_users_by_email, \
               len_matched_users_by_email_and_name, \
               authors_updated, \
               users_inserted, \
               users_merged_count, \
               authors_merged_count


def identify_authors_to_merge(authors):
    users = create_users_dict(authors)
    matcher = EmailMatcher()
    len_users = len(users.values())
    len_authors = len(authors)

    matched_users_by_email = match(users.values(), matcher)

    users_merged_count_by_email, authors_merged_count_by_email = merge_users(matched_users_by_email)
    len_matched_users_by_email = len(matched_users_by_email)

    matcher = EmailNameMatcher()
    matched_users_by_email_and_name = match(list(itertools.chain.from_iterable(matched_users_by_email)), matcher)

    users_merged_count_by_email_and_name, authors_merged_count_by_email_and_name = merge_users(matched_users_by_email_and_name)
    len_matched_users_by_email_and_name = len(matched_users_by_email_and_name)
    users_merged_count = authors_merged_count_by_email+users_merged_count_by_email_and_name
    authors_merged_count = authors_merged_count_by_email + authors_merged_count_by_email_and_name

    return len_matched_users_by_email, len_matched_users_by_email_and_name, len_users, len_authors, matched_users_by_email_and_name, users_merged_count, authors_merged_count

def identify_authors_to_merge_with_human_help(authors, confidence_level: float):
    users = create_users_dict(authors)

    len_users = len(users.values())
    len_authors = len(authors)

    matcher = EmailNameMatcher(confidence_level=confidence_level)
    matched_users_by_email_and_name = match(users.values(), matcher)

    users_merged_count_by_email_and_name, authors_merged_count_by_email_and_name = merge_users(matched_users_by_email_and_name, get_bool_input)
    len_matched_users_by_email_and_name = len(matched_users_by_email_and_name)

    return 0, len_matched_users_by_email_and_name, len_users, len_authors, matched_users_by_email_and_name, users_merged_count_by_email_and_name, authors_merged_count_by_email_and_name

def identity_merge_users_with_human_help(project, verbose: bool = False):
    authors = load_authors_for_project(project)

    len_matched_users_by_email, \
    len_matched_users_by_email_and_name, \
    len_users, \
    len_authors, \
    matched_users_by_email_and_name, \
    users_merged_count, \
    authors_merged_count = identify_authors_to_merge_with_human_help(authors, 0.7)

    authors_updated, users_inserted = save_identified_merged_users(matched_users_by_email_and_name)
    if verbose:
        print(matched_users_by_email_and_name)

    return len_users, \
           len_authors, \
           len_matched_users_by_email, \
           len_matched_users_by_email_and_name, \
           authors_updated, \
           users_inserted, \
           users_merged_count, \
           authors_merged_count


def save_identified_merged_users(users):
    authors_updated = 0
    users_inserted = 0
    for user_sublist in tqdm(iterable=users, desc="Saving users"):
        if isinstance(user_sublist, list):
            for user in user_sublist:
                if user.is_active == False:
                    new_user = create_new_user(user)
                    if (new_user is not None
                            and new_user.id is not None):
                        # handle the case where there is an existing user in DB with the same primary email as the one being inserted
                        if user.id != new_user.id:
                            user.id = new_user.id
                        else:
                            users_inserted+=1
                for author in user.identities:
                    # handle the case where there is an existing user in DB with the same primary email as the one being inserted
                    if user.id != author.user_id:
                        author.user_id = user.id
                    if author.aliases == '1':
                        authors_updated += assign_author_to_user_profile(author)
    return authors_updated, users_inserted

def create_users_dict(authors):
    users = {}
    for author in authors.values():
        # ignore authors with emails to be ignored
        if is_ignored_email(author.email) or \
                is_ignored_name(author.name):
            continue

        # There are two cases:
        if author.user_id is not None:
            # 1. the User this author is assigned to DOES exist in the database

            if author.user_id not in users:

                # is_active indicates the User DOES exist in the database
                user = User(
                    id=author.user_id,
                    name=author.name,
                    is_active=True
                )
                users[user.id] = user
            else:
                user = users[author.user_id]

            user.identities.append(author)

        else:
            # 2. the User this author is assigned to DOES NOT exist in the database
            # is_active indicates the User DOES NOT exist in the database
            user = User(
                name=author.name,
                is_active=False
            )
            author.user_id = user.id
            user.identities = [author]
            users[user.id] = user

        # generate no-reply email for the user
        try:
            EmailStr.validate(author.email)
            user.primary_email = author.email
        except EmailError:
            user.primary_email = generate_no_reply_user_email_address(user.id, user.name)

    return users


def merge_users(matched_users_list, confirmation_func = auto_confirmation):

    authors_merged_count = 0
    users_merged_count = 0
    for user_sublist in matched_users_list:
        if isinstance(user_sublist, list) and len(user_sublist) > 1:
            # sort the list so that users that are in the database to be assigned the other users
            user_sublist.sort(key=lambda x: (x.is_active, len(x.name)), reverse=True)
            for index in range(1, len(user_sublist)):
                user = user_sublist.pop()
                for identity in user.identities:
                    if confirmation_func(
                            '\nDo you want to merge this author: {} \n into this user: {} \n with email:{} ?(yes/no)'.
                                    format(identity.canonical_name, user_sublist[0].name, user_sublist[0].primary_email)
                    ):
                        user_sublist[0].identities.extend([identity])
                        users_merged_count += 1
                for author in user_sublist[0].identities:
                    if author.user_id != user_sublist[0].id:
                            authors_merged_count +=1
                            author.aliases='1'
                    author.user_id = user_sublist[0].id
    return users_merged_count, authors_merged_count