from pydantic import EmailStr

from kedehub_client import get_sync_apis

def create_new_user(user):
    new_user = get_sync_apis().user_api.post_create_new_user(user)
    return new_user

def load_user_by_email(email: EmailStr):
    user = get_sync_apis().user_api.find_user_by_email(email)
    return user