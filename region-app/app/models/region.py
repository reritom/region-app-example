from app.database import db

class Region(db.Model):
    __tablename__ = "regions"

    # One would think the code would be an integer, but the dataset seems to suggest it could be a string
    code = db.Column(db.String(10), primary_key=True, unique=True)
    name = db.Column(db.String(36), primary_key=True)

    # Children
    counties = db.relationship("County", back_populates="region", lazy=True)

    @property
    def total_population(self):
        # Get the total population by summing the child cities of the child regions
        total = 0
        for county in self.counties:
            for city in county.cities:
                total += city.population
        return total

    @property
    def total_area(self):
        # Get the total area by summing the child cities of the child regions
        total = 0
        for county in self.counties:
            for city in county.cities:
                total += city.area
        return total
