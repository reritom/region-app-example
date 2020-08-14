from app.database import db

class Region(db.Model):
    __tablename__ = "regions"

    # One would think the code would be an integer, but the dataset seems to suggest it could be a string
    code = db.Column(db.String(10), primary_key=True, unique=True)
    name = db.Column(db.String(36), primary_key=True)

    # Children
    counties = db.relationship("County", back_populates="region", lazy=True)
