from typing import Optional
from app.models import Region
import json

class RegionSerialiser:
    @staticmethod
    def serialise(region: Region, osm_details: Optional[dict] = None) -> dict:
        serialised_region = {
            "name": region.name,
            "code": region.code,
            "totalPopulation": str(region.total_population),
            "totalArea": str(region.total_area)
        }

        if osm_details:
            # We will enrich with the latitude and longitude
            serialised_region["lat"] = osm_details.get("lat")
            serialised_region["lon"] = osm_details.get("lon")

        return serialised_region
