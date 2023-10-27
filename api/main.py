# api/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .routes.auth import session as session_router
from .routes.dashboard import dashboard as dashboard_router
from .config import project_dir, setup_logging

# Initialize logging
setup_logging()

# Load environment variables from .env file
load_dotenv()

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# Add the SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("CLIENT_SECRET"),  # Load secret from environment variable
    max_age=30 * 24 * 60 * 60  # 30 days
)

# Mount the static files with absolute paths
app.mount("/assets", StaticFiles(directory=os.path.join(project_dir, 'frontend', 'assets')), name="assets")

# Include routers
app.include_router(session_router)
app.include_router(dashboard_router)