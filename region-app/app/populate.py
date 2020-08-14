from app.models import Region, County, City
from app.database import db
import pandas as pd
from sqlalchemy import exc
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def populate(csv_path):
    """
    This function is used for populating the application database with the data in the provided csv path.
    As of writing this, the function does Not handle re-seeding with an updated version of the same dataset.
    """
    logger.info("Populating")
    csv_dataframe = pd.read_csv(csv_path, delimiter=";")

    # We will store our temporary models here to avoid duplications
    cities = {}
    counties = {}
    regions = {}

    # Each row seems to reflect a city, so we create a city for each row.
    for index, row in csv_dataframe.iterrows():
        # Take some keys to be used as foreign keys
        county_code = str(csv_dataframe.at[index, "Code Département"])
        region_code = str(csv_dataframe.at[index, "Code Région"])

        city = City(
            code_insee=csv_dataframe.at[index, "Code INSEE"],
            population=csv_dataframe.at[index, "Population"],
            code_postal=csv_dataframe.at[index, "Code Postal"],
            name=csv_dataframe.at[index, "Commune"],
            area=csv_dataframe.at[index, "Superficie"],
            county_code=county_code
        )
        cities[city.code_insee] = city

        # If this county hasn't been encountered yet, we will create a model for it
        if not county_code in counties:
            county = County(
                code=county_code,
                name=csv_dataframe.at[index, "Département"],
                region_code=region_code
            )
            counties[county_code] = county

        # If this region hasn't been encountered yet, we will create a model for it
        if not region_code in regions:
            region = Region(
                code=region_code,
                name=csv_dataframe.at[index, "Région"]
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
