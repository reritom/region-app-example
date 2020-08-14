import requests
from typing import Optional
from cachetools import cached


class OSMApi:
    # Class for interacting with the OpenStreetMap API
    SEARCH_URL = "https://nominatim.openstreetmap.org/search"

    @staticmethod
    @cached(cache={})
    def get_state_details(country: str, state: str) -> Optional[dict]:
        """
        For a given country and state, retreive the details from the API and return either a dictionary or None.
        Note: in the name of this method we use the nomenclature of the API, despite us internally using region instead of state.
        The above note is a design choice which is down to preference, but open to change.
        """
        params = {"country": country, "state": state, "format": "json"}
        response = requests.get(f"{OSMApi.SEARCH_URL}", params=params)
        
        if response.ok:
            # TODO: Typically I would return a dataclass here created from the JSON, but it is currently out of scope.
            # The API returns a list of none/one (and maybe more) items
            # TODO determine whether we need to handle cases where there are more than 1 items
            response_json = response.json()
            return response_json[0] if response_json else None
