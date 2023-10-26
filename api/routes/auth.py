# File: api/routes/auth.py

import os
import logging
from fastapi import APIRouter, Form, HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from api.models.users import RegistrationForm, LoginForm
from api.modules.db import fetch_all_users, save_user, get_user_by_email, get_user_count
from api.modules.encryption import hash_password, verify_password
from api.modules.authentication import get_current_user
from api.config import authPages, setup_logging, debugStatus

# Initialize logging
setup_logging()

session = APIRouter()

def is_debug_mode() -> None:
    if debugStatus != "True":
        raise HTTPException(status_code=403, detail="Only accessible in Development Mode")

# USED FOR DEVELOPMENT ONLY
@session.get("/auth/users")
async def list_users(is_debug: None = Depends(is_debug_mode)):
    users = await fetch_all_users()
    return {"users": users}

@session.get("/auth/users/{email}")
async def list_single_users(email: str, is_debug: None = Depends(is_debug_mode)):
    user = await get_user_by_email(email)
    if user:
        user.pop('password', None)
        user.pop('_id', None)
    return {"user": user}

@session.get("/auth/signin", response_class=HTMLResponse)
async def show_signin_form(request: Request, current_user: dict = Depends(get_current_user)):
    login_error = request.session.pop("login_error", None)
    if current_user is None:
        return authPages.TemplateResponse("sign-in.html", {"request": request, "login_error": login_error})
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@session.get("/auth/register", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    return authPages.TemplateResponse("sign-up.html", {"request": request})

def redirect_with_status(url: str, status_code: int = status.HTTP_303_SEE_OTHER):
    return RedirectResponse(url=url, status_code=status_code)

@session.post("/auth/user-register")
async def handle_registration(
        fullname: str = Form(...),
        contact_no: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        terms_and_conditions: bool = Form(...)):
    if not terms_and_conditions:
        raise HTTPException(status_code=400, detail="You must accept the terms and conditions")
    
    hashed_password = hash_password(password)
    
    # If first user, make them admin
    user_count = await get_user_count()
    if user_count == 0:
        baseGroup = "admin"
        basePermission = "all"
    else:
        baseGroup = "users"
        basePermission = "basic"

    form_data = RegistrationForm(
        fullname=fullname,
        contact_no=contact_no,
        email=email,
        password=hashed_password,
        terms_and_conditions=terms_and_conditions,
        groups=baseGroup,
        permission=basePermission
    )

    await save_user(form_data.dict())
    return redirect_with_status("/")

@session.post("/auth/user-signin")
async def handle_login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = await get_user_by_email(email)
    if user is None or not verify_password(password, user["password"]):
        logging.error("Login failed")
        request.session["login_error"] = "Invalid credentials"
        return redirect_with_status("/auth/signin")
    logging.info("Login successful")
    request.session["user_email"] = user["email"]  # Storing user email in session
    return redirect_with_status("/")

@session.get("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return redirect_with_status("/auth/signin")
