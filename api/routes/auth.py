# File: api/routes/auth.py

import os
import logging
from fastapi import APIRouter, Form, HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..models.users import RegistrationForm, LoginForm
from ..modules.db import fetch_all_users, save_user, get_user_by_email
from ..modules.encryption import hash_password, verify_password
from ..modules.authentication import get_current_user

session = APIRouter()

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
authPages = Jinja2Templates(directory=os.path.join(project_dir, 'frontend', 'dashboard', 'auth'))

@session.get("/auth/users")
async def list_users():
    users = await fetch_all_users()
    return {"users": users}

@session.get("/auth/signin", response_class=HTMLResponse)
async def read_root(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        return authPages.TemplateResponse("sign-in.html", {"request": request})
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@session.get("/auth/register", response_class=HTMLResponse)
async def read_root(request: Request):
    return authPages.TemplateResponse("sign-up.html", {"request": request})

@session.post("/auth/user-register")
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

@session.post("/auth/user-signin")
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

@session.get("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/auth/signin")