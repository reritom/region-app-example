import os
import logging
from app import create_app

if __name__=="__main__":
    app = create_app(db_uri="sqlite:///app.sqlite3")
    app.run("0.0.0.0", port=8080, debug=False)
