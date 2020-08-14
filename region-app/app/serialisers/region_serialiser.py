

class RegionSerialiser:
    @staticmethod
    def serialise(region) -> dict:
        return {
            "name": region.name,
            "code": region.code
        }
