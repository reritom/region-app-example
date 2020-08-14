from app.database import db

class Region(db.Model):
    __tablename__ = "regions"

    code = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(36), primary_key=True)

    # Children
    counties = db.relationship("County", back_populates="region", lazy=True)
