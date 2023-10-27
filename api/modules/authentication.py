# File: api/modules/authentication.py

from starlette.requests import Request
from .db import get_user_by_email
from ..config import setup_logging

# Initialize logging
setup_logging()

def get_current_user(request: Request):
    email = request.session.get("user_email")
    if email is None:
        return None  # User is not authenticated
    return email  # Return the authenticated user

# Update to async function to await get_user_by_email
async def get_user_name(request: Request):
    email = request.session.get("user_email")
    if email is None:
        return None  # User is not authenticated

    user = await get_user_by_email(email)  # Awaiting the asynchronous function
    if user is None:
        return None  # User data could not be found, consider this as not authenticated

    return user["fullname"]