from uuid import UUID

# format ID@users.noreply.kedegub.io
def generate_no_reply_user_email_address(id: UUID, name: str):

    return str(id)+"@users.noreply.kedegub.io"