import os
import logging
from app import create_app

app = create_app()
app.run("0.0.0.0", port=8080, debug=False)
