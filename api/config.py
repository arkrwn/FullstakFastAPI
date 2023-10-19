# File: api/config.py

import os
import logging
from datetime import datetime
from fastapi.templating import Jinja2Templates

current_year = datetime.now().year
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dashboardPages = Jinja2Templates(directory=os.path.join(project_dir, 'frontend', 'dashboard'))
authPages = Jinja2Templates(directory=os.path.join(project_dir, 'frontend', 'dashboard', 'auth'))

def setup_logging():
    logging.basicConfig(level=logging.ERROR)
