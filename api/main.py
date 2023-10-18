# api/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .routes.auth import session as session_router
from .routes.dashboard import dashboard as dashboard_router
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
current_year = datetime.now().year

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# Get the absolute path to the project directory
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Include routers
app.include_router(session_router)
app.include_router(dashboard_router)

# Add the SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("CLIENT_SECRET"),  # Load secret from environment variable
    max_age=30 * 24 * 60 * 60  # 30 days
)

# Mount the static files with absolute paths
app.mount("/assets", StaticFiles(directory=os.path.join(project_dir, 'frontend', 'assets')), name="assets")