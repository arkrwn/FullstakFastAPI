# File: api/routes/dashboard.py

import os
from pathlib import Path
from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api.modules.authentication import get_current_user
from api.config import frontendDirectory, dashboardPages, setup_logging, webTitle

# Initialize logging
setup_logging()

dashboard = APIRouter()

# USE THIS DURING DEVELOPMENT ONLY
@dashboard.get("/documentations", response_class=HTMLResponse)
async def read_documentations(request: Request):
    pageTitle = f"{webTitle} | Documentations"
    return dashboardPages.TemplateResponse("documentations.html", {"request": request, "title": webTitle})

@dashboard.get("/errors/{error_code}", response_class=HTMLResponse)
async def read_error(request: Request, error_code: int):
    if error_code not in [404, 500, 503]:
        raise HTTPException(status_code=404, detail="Error page not found")
    
    pageTitle = f"{webTitle} | Errors"
    template_name = f"error{error_code}.html"
    return dashboardPages.TemplateResponse(template_name, {"request": request, "title": pageTitle})

@dashboard.get("/", response_class=HTMLResponse)
async def read_root(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/auth/signin", status_code=status.HTTP_303_SEE_OTHER)
    pageTitle = f"{webTitle} | index".upper()
    return dashboardPages.TemplateResponse("index.html", {"request": request, "title": pageTitle})
    
@dashboard.get("/{path:path}/{filename}", response_class=HTMLResponse)
async def read_file(request: Request, path: str, filename: str, current_user: dict = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/auth/signin", status_code=status.HTTP_303_SEE_OTHER)

    # Compute the dynamic directory based on request
    dynamic_dir = os.path.join(frontendDirectory, path)

    # Initialize Jinja2Templates with the dynamic directory
    dynamicPages = Jinja2Templates(directory=dynamic_dir)
    file_path = f"{filename}.html"
    pageTitle = f"{webTitle} | {filename}".upper()

    try:
        return dynamicPages.TemplateResponse(file_path, {"request": request, "title": pageTitle})
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")