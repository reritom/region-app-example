from flask import request, jsonify
from app.models import Region
from app.serialisers import RegionSerialiser
import logging

logger = logging.getLogger(__name__)


class RegionController:
    @staticmethod
    def get_regions():
        """
        Method for retreiving the regions from the database and returning each, serialised
        """
        regions = (
            Region.query.paginate(page=int(request.args["page"]), per_page=int(request.args["limit"])).items
            if request.args.get("page") and request.args.get("limit")
            else Region.query.all()
        )
        serialised_regions = [RegionSerialiser.serialise(region) for region in regions]
        return jsonify(serialised_regions), 200
