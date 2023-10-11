from pydantic import BaseModel

class RegistrationForm(BaseModel):
    fullname: str
    contact_no: str
    email: str
    password: str
    terms_and_conditions: bool

class LoginForm(BaseModel):
    email: str
    password: str
    remember_me: bool
