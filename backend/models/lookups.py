from .base import db

class ChestPainType(db.Model):
    """Lookup table for chest pain type classifications."""
    __tablename__ = "chest_pain_type"

    cp_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    patients = db.relationship("Patient", back_populates="chest_pain")


class ThalType(db.Model):
    """Lookup table for thalassemia type classifications."""
    __tablename__ = "thal_type"

    thal_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    patients = db.relationship("Patient", back_populates="thal")


class RestecgType(db.Model):
    """Lookup table for resting ECG result classifications."""
    __tablename__ = "restecg_type"

    restecg_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    patients = db.relationship("Patient", back_populates="restecg")


class SlopeType(db.Model):
    """Lookup table for slope of peak exercise ST segment classifications."""
    __tablename__ = "slope_type"

    slope_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    patients = db.relationship("Patient", back_populates="slope")