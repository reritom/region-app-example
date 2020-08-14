import os
import logging
from app import create_app

# This module is used when running the application using gunicorn
app = create_app()
