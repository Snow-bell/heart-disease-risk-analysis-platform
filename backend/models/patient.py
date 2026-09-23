from .base import db

class Patient(db.Model):
    """Patient records with clinical measurements and heart disease diagnosis."""
    __tablename__ = "patient"

    patient_id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    cp_id = db.Column(db.Integer, db.ForeignKey("chest_pain_type.cp_id"))
    trestbps = db.Column(db.Integer)
    chol = db.Column(db.Integer)
    fbs = db.Column(db.Integer)
    restecg_id = db.Column(db.Integer, db.ForeignKey("restecg_type.restecg_id"))
    thalach = db.Column(db.Integer)
    exang = db.Column(db.Integer)
    oldpeak = db.Column(db.Float)
    slope_id = db.Column(db.Integer, db.ForeignKey("slope_type.slope_id"))
    ca = db.Column(db.Integer)
    thal_id = db.Column(db.Integer, db.ForeignKey("thal_type.thal_id"))
    heart_disease_present = db.Column(db.Integer, nullable=False)

    chest_pain = db.relationship("ChestPainType", back_populates="patients")
    thal = db.relationship("ThalType", back_populates="patients")
    restecg = db.relationship("RestecgType", back_populates="patients")
    slope = db.relationship("SlopeType", back_populates="patients")