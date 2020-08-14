from flask import request, jsonify
from app.models import Region
from app.serialisers import RegionSerialiser
from app.apis import OSMApi
from app.tools.constants import COUNTRY_FRANCE
import logging

logger = logging.getLogger(__name__)


class RegionController:
    @staticmethod
    def get_regions():
        """
        Method for retreiving the regions from the database and returning each, serialised.
        The region models we have will be enriched by the OSMApi if possible.
        The OSMApi uses caches, so the first call to this API will be slower than the subsequent ones.
        Ideally the OSMApi data should be replicated on our side because it appears static.
        """
        regions = (
            Region.query.paginate(page=int(request.args["page"]), per_page=int(request.args["limit"])).items
            if request.args.get("page") and request.args.get("limit")
            else Region.query.all()
        )

        # The region details from OSM don't exist as part of the Region model
        # So we can't just tack them onto the model and pass them serialiser
        # However, we can pass enrichments to the serialiser
        serialised_regions = [
            RegionSerialiser.serialise(
                region=region,
                osm_details=OSMApi.get_state_details(country=COUNTRY_FRANCE, state=region.name))
            for region in regions
        ]
        return jsonify(serialised_regions), 200
