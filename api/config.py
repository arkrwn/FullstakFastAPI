# File: api/config.py

import os
import logging
from datetime import datetime
from fastapi.templating import Jinja2Templates

webTitle = "ARKWRN"
debugStatus = "True"
current_year = datetime.now().year
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
frontendDirectory=os.path.join(project_dir, 'frontend')
dashboardPages = Jinja2Templates(os.path.join(frontendDirectory, 'dashboard'))
authPages = Jinja2Templates(os.path.join(frontendDirectory, 'dashboard', 'auth'))

def setup_logging():
    logging.basicConfig(level=logging.ERROR)
