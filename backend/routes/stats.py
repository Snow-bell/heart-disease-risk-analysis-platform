from flask import Blueprint, jsonify
from models.base import db
from models.patient import Patient
from sqlalchemy import func

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/summary")
def get_summary():
    """Return overall dataset statistics."""
    total = Patient.query.count()
    with_disease = Patient.query.filter(Patient.heart_disease_present > 0).count()
    avg_age = db.session.query(func.avg(Patient.age)).scalar()
    avg_chol = db.session.query(func.avg(Patient.chol)).scalar()
    avg_bp = db.session.query(func.avg(Patient.trestbps)).scalar()

    return jsonify({
        "total_patients": total,
        "with_heart_disease": with_disease,
        "without_heart_disease": total - with_disease,
        "heart_disease_percentage": round(with_disease / total * 100, 2),
        "avg_age": round(avg_age, 2),
        "avg_cholesterol": round(avg_chol, 2),
        "avg_blood_pressure": round(avg_bp, 2)
    })


@stats_bp.route("/by-age")
def get_by_age():
    """Return heart disease presence grouped by age range."""
    patients = Patient.query.all()
    
    age_groups = {
        "29-40": {"total": 0, "with_disease": 0},
        "41-50": {"total": 0, "with_disease": 0},
        "51-60": {"total": 0, "with_disease": 0},
        "61-77": {"total": 0, "with_disease": 0},
    }

    for p in patients:
        if 29 <= p.age <= 40:
            group = "29-40"
        elif 41 <= p.age <= 50:
            group = "41-50"
        elif 51 <= p.age <= 60:
            group = "51-60"
        else:
            group = "61-77"

        age_groups[group]["total"] += 1
        if p.heart_disease_present > 0:
            age_groups[group]["with_disease"] += 1

    return jsonify(age_groups)


@stats_bp.route("/by-chest-pain")
def get_by_chest_pain():
    """Return heart disease presence grouped by chest pain type."""
    results = db.session.query(
        Patient.cp_id,
        func.count(Patient.patient_id).label("total"),
        func.sum(
            db.case((Patient.heart_disease_present > 0, 1), else_=0)
        ).label("with_disease")
    ).group_by(Patient.cp_id).all()

    from models.lookups import ChestPainType
    return jsonify([{
        "chest_pain_type": ChestPainType.query.get(r.cp_id).description if r.cp_id else None,
        "total": r.total,
        "with_disease": r.with_disease
    } for r in results])


@stats_bp.route("/by-sex")
def get_by_sex():
    """Return heart disease presence grouped by sex."""
    results = db.session.query(
        Patient.sex,
        func.count(Patient.patient_id).label("total"),
        func.sum(
            db.case((Patient.heart_disease_present > 0, 1), else_=0)
        ).label("with_disease")
    ).group_by(Patient.sex).all()

    return jsonify([{
        "sex": "Male" if r.sex == 1 else "Female",
        "total": r.total,
        "with_disease": r.with_disease
    } for r in results])


@stats_bp.route("/by-thal")
def get_by_thal():
    """Return heart disease presence grouped by thalassemia type."""
    results = db.session.query(
        Patient.thal_id,
        func.count(Patient.patient_id).label("total"),
        func.sum(
            db.case((Patient.heart_disease_present > 0, 1), else_=0)
        ).label("with_disease")
    ).group_by(Patient.thal_id).all()

    from models.lookups import ThalType
    return jsonify([{
        "thal_type": ThalType.query.get(r.thal_id).description if r.thal_id else None,
        "total": r.total,
        "with_disease": r.with_disease
    } for r in results])


@stats_bp.route("/risk-factors")
def get_risk_factors():
    """Return average clinical measurements grouped by heart disease presence."""
    results = db.session.query(
        Patient.heart_disease_present,
        func.avg(Patient.chol).label("avg_chol"),
        func.avg(Patient.trestbps).label("avg_bp"),
        func.avg(Patient.thalach).label("avg_thalach"),
        func.avg(Patient.age).label("avg_age")
    ).group_by(Patient.heart_disease_present).all()

    return jsonify([{
        "heart_disease_present": r.heart_disease_present,
        "avg_cholesterol": round(r.avg_chol, 2),
        "avg_blood_pressure": round(r.avg_bp, 2),
        "avg_max_heart_rate": round(r.avg_thalach, 2),
        "avg_age": round(r.avg_age, 2)
    } for r in results])