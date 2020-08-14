from flask import request, jsonify
from app.models import Region
from app.serialisers import RegionSerialiser


class RegionController:
    @staticmethod
    def get_regions():
        regions = Region.query.all()
        print(f"There are {len(regions)} regions")
        regions = [RegionSerialiser.serialise(region) for region in regions]
        print(regions)
        return jsonify(regions), 200
