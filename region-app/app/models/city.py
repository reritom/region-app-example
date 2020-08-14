from app.database import db

class City(db.Model):
    __tablename__ = "cities"

    code_insee = db.Column(db.String(10), primary_key=True, unique=True)
    code_postal = db.Column(db.String(50), primary_key=True) # Long string because some examples seem to have chained post codes
    name = db.Column(db.String(100), primary_key=True)
    population = db.Column(db.Float(asdecimal=True))
    area = db.Column(db.Float(asdecimal=True))

    # Parents
    county_code = db.Column(db.ForeignKey('counties.code'))
    county = db.relationship('County', foreign_keys=county_code)
