# api/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_303_SEE_OTHER
from .modules.authentication import get_current_user, get_user_name
from .models.users import RegistrationForm
from .routes.session import router as session_router
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
current_year = datetime.now().year

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# Get the absolute path to the project directory
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Include routers
app.include_router(session_router)

# Add the SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("CLIENT_SECRET"),  # Load secret from environment variable
    max_age=30 * 24 * 60 * 60  # 30 days
)

# Mount the static files with absolute paths
app.mount("/assets", StaticFiles(directory=os.path.join(project_dir, 'frontend', 'assets')), name="assets")
app.mount("/theme-assets", StaticFiles(directory=os.path.join(project_dir, 'frontend', 'theme-assets')), name="theme-assets")

# Mount the favicon.ico
app.mount("/favicon.ico", StaticFiles(directory=os.path.join(project_dir, 'frontend', 'theme-assets')), name="favicon")

# Set up templates with absolute paths
templates = Jinja2Templates(directory=os.path.join(project_dir, 'frontend', 'pages'))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        # If the user is not authenticated, redirect to the login page
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)  
    
    user_name = await get_user_name(request)
    # If the user is authenticated, display the dashboard
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_name": user_name, "current_year": current_year})

@app.get("/login", response_class=HTMLResponse)
async def read_root(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        # If the user is not authenticated, redirect to the login page
        return templates.TemplateResponse("login.html", {"request": request})
    
    # If the user is authenticated, display the dashboard
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@app.get("/register", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/{filename}", response_class=HTMLResponse)
async def read_file(filename: str, request: Request, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        # If the user is not authenticated, redirect to the login page
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    
    # List of available HTML files
    available_files = [
        "buttons", "cards", "charts", "form-elements", 
        "icons", "page", "tables", "typography"
    ]
    
    if filename in available_files:
        user_name = await get_user_name(request)
        return templates.TemplateResponse(f"{filename}.html", {"request": request, "user_name": user_name, "current_year": current_year})
    else:
        # If the filename is not in the list of available files, return a 404 Not Found error
        return HTMLResponse(status_code=404, content="<html><body><h1>404 Not Found</h1></body></html>")