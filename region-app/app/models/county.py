from app.database import db

class County(db.Model):
    __tablename__ = "counties"

    # One would think the code would be an integer, but the dataset seems to suggest it could be a string
    code = db.Column(db.String(10), primary_key=True, unique=True)
    name = db.Column(db.String(36), primary_key=True)

    # Parents
    region_code = db.Column(db.ForeignKey('regions.code'))
    region = db.relationship('Region', foreign_keys=region_code)

    # Children
    cities = db.relationship("City", back_populates="county", lazy=True)
