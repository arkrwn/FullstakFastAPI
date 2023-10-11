# File: api/routes/session.py

from fastapi import APIRouter, Form, HTTPException, status, Request
from starlette.responses import RedirectResponse
from ..models.users import RegistrationForm, LoginForm
from ..modules.db import fetch_all_users, save_user, get_user_by_email
from ..modules.encryption import hash_password, verify_password

router = APIRouter()

@router.get("/users")
async def list_users():
    users = await fetch_all_users()
    return {"users": users}

@router.post("/register-user")
async def handle_registration(
        fullname: str = Form(...),
        contact_no: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        terms_and_conditions: bool = Form(...)):
    hashed_password = hash_password(password)
    form_data = RegistrationForm(
        fullname=fullname,
        contact_no=contact_no,
        email=email,
        password=hashed_password,
        terms_and_conditions=terms_and_conditions
    )
    if not form_data.terms_and_conditions:
        raise HTTPException(status_code=400, detail="You must accept the terms and conditions")
    inserted_id = await save_user(form_data.dict())
    return {"message": "User registered successfully", "_id": str(inserted_id)}

@router.post("/login-user")
async def handle_login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        remember_me: bool = Form(False)):
    user = await get_user_by_email(email)
    if user is None or not verify_password(password, user["password"]):
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        # Add a session variable to indicate login failure
        request.session["login_error"] = "Invalid credentials"
        return response
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return response
