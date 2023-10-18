# File: api/routes/session.py

import os
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..modules.authentication import get_current_user

dashboard = APIRouter()

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
dashboardPages = Jinja2Templates(directory=os.path.join(project_dir, 'frontend', 'dashboard'))

@dashboard.get("/documentations", response_class=HTMLResponse)
async def read_root(request: Request):
    return dashboardPages.TemplateResponse("documentations.html", {"request": request})

@dashboard.get("/", response_class=HTMLResponse)
async def read_root(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/auth/signin", status_code=status.HTTP_303_SEE_OTHER)

    return dashboardPages.TemplateResponse("index.html", {"request": request})