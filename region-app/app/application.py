from flask import Flask
from app.database import db
from app.controllers import RegionController
import logging


logger = logging.getLogger(__name__)

def create_app(db_uri: str) -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # For region related endpoints
    app.add_url_rule('/api/regions', methods=['GET'], view_func=RegionController.get_regions)

    return app
