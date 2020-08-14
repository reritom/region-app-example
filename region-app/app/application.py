from flask import Flask
from flask.cli import with_appcontext
import click
import os
from app.database import db
from app.controllers import RegionController
from app.populate import populate
import logging


logger = logging.getLogger(__name__)

def create_app() -> Flask:
    """
    Application factory, returns an instance of a Flask App.
    This could be expanded to receive a config object.
    """
    # Retrieve the database uri
    db_uri = os.environ.get("db_uri")
    if not db_uri:
        raise SystemError("No db_uri set in the environment")

    logger.info("Creating application with database uri %s", db_uri)
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False
    db.init_app(app)

    # Add a cli command for populating data
    app.cli.add_command(seed)

    # Create all the models in our database if they aren't already present
    # TODO: This should be handled externally, outside of our ORM.
    with app.app_context():
        db.create_all()

    # For region related endpoints
    app.add_url_rule('/api/regions', methods=['GET'], view_func=RegionController.get_regions)

    return app


# We will add a command line function for populating the database with the data from a given csv
@click.command()
@click.argument("csv_path")
@with_appcontext
def seed(csv_path):
    db.create_all()
    populate(csv_path)
