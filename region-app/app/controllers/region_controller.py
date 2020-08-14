from flask import request, jsonify


class RegionController:
    @staticmethod
    def get_regions():
        return jsonify({}), 200
