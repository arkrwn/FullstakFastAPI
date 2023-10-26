# File: api/models/users.py

from pydantic import BaseModel
from datetime import datetime

class RegistrationForm(BaseModel):
    fullname: str
    contact_no: str
    email: str
    password: str
    terms_and_conditions: bool
    user_profile_picture: str = ""
    groups: str
    permission: str
    register_date: datetime = datetime.utcnow()
    status: str = "active"
    two_factor: str = "disabled"
    two_factor_token: str = ""

class LoginForm(BaseModel):
    email: str
    password: str
    remember_me: bool
