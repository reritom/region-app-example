import os
import logging
from app import create_app

# This module is used when running the application directly using Flasks builtin server (not gunicorn)
app = create_app()
app.run("0.0.0.0", port=8080, debug=False)
