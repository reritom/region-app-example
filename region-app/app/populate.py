from app.models import Region, County, City
from app.database import db
import csv
from sqlalchemy import exc
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def row_to_dict(headers, row):
    return {headers[index]: row[index] for index, _ in enumerate(headers)}


def populate(csv_path):
    """
    This function is used for populating the application database with the data in the provided csv path.
    As of writing this, the function does Not handle re-seeding with an updated version of the same dataset.
    """
    logger.info("Populating")

    # We will store our temporary models here to avoid duplications
    cities = {}
    counties = {}
    regions = {}

    # Each row seems to reflect a city, so we create a city for each row.
    with open(csv_path, 'r') as f:
        reader = csv.reader(f, delimiter=";")

        for index, row in enumerate(reader):
            if index == 0:
                headers = row
                continue

            # Convert the row into a more usable format
            row_dict = row_to_dict(headers, row)

            # Take some keys to be used as foreign keys
            county_code = str(row_dict["Code Département"])
            region_code = str(row_dict["Code Région"])

            city = City(
                code_insee=row_dict["Code INSEE"],
                population=row_dict["Population"],
                code_postal=row_dict["Code Postal"],
                name=row_dict["Commune"],
                area=row_dict["Superficie"],
                county_code=county_code
            )
            cities[city.code_insee] = city

            # If this county hasn't been encountered yet, we will create a model for it
            if not county_code in counties:
                county = County(
                    code=county_code,
                    name=row_dict["Département"],
                    region_code=region_code
                )
                counties[county_code] = county

            # If this region hasn't been encountered yet, we will create a model for it
            if not region_code in regions:
                region = Region(
                    code=region_code,
                    name=row_dict["Région"]
                )
                regions[region_code] = region

    logger.info("There are %s cities", len(cities))
    logger.info("There are %s counties", len(counties))
    logger.info("There are %s regions", len(regions))

    # We will use add_all for now, but it means we can't repopulate due to IntegrityErrors
    items = (
        [city for _, city in cities.items()]
        + [county for _, county in counties.items()]
        + [region for _, region in regions.items()]
    )

    db.session.add_all(items)
    try:
        db.session.commit()
    except exc.IntegrityError:
        logger.error("Failed to add the resources to the database as some already exist")
        db.session.rollback()
