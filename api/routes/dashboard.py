# File: api/routes/dashboard.py

import os
from pathlib import Path
from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..modules.authentication import get_current_user

dashboard = APIRouter()

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
dashboardPages = Jinja2Templates(directory=os.path.join(project_dir, 'frontend', 'dashboard'))

# USE THIS DURING DEVELOPMENT ONLY
@dashboard.get("/documentations", response_class=HTMLResponse)
async def read_root(request: Request):
    return dashboardPages.TemplateResponse("documentations.html", {"request": request})

@dashboard.get("/", response_class=HTMLResponse)
async def read_root(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/dashboard/auth/sign-in", status_code=status.HTTP_303_SEE_OTHER)

    return dashboardPages.TemplateResponse("index.html", {"request": request})
    
@dashboard.get("/{path:path}/{filename}", response_class=HTMLResponse)
async def read_file(path: str, filename: str, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/dashboard/auth/sign-in", status_code=status.HTTP_303_SEE_OTHER)
    
    # Construct the path to the file
    path_str = os.path.join("frontend", path, f"{filename}.html")
    path = Path(path_str)
    
    # Verify if the file exists
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Read and return the HTML content
    with open(path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)