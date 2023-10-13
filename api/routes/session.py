# File: api/routes/session.py

import logging
from fastapi import APIRouter, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse
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
    registered = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return registered

@router.post("/login-user")
async def handle_login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        remember_me: bool = Form(False)):
    user = await get_user_by_email(email)
    if user is None or not verify_password(password, user["password"]):
        logging.error("Login failed")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        request.session["login_error"] = "Invalid credentials"
        return response
    logging.info("Login successful")
    request.session["user_email"] = user["email"]  # Storing user email in session
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return response


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")