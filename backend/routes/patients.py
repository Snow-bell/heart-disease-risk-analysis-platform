from flask import Blueprint, jsonify, request
from models.patient import Patient
from models.lookups import ChestPainType, ThalType, RestecgType, SlopeType

patients_bp = Blueprint("patients", __name__)


@patients_bp.route("/", methods=["GET"])
def get_patients():
    """Return all patients with optional filtering by query parameters."""
    query = Patient.query

    sex = request.args.get("sex")
    heart_disease = request.args.get("heart_disease_present")
    cp = request.args.get("cp")

    if sex is not None:
        query = query.filter(Patient.sex == int(sex))
    if heart_disease is not None:
        query = query.filter(Patient.heart_disease_present == int(heart_disease))
    if cp is not None:
        cp_type = ChestPainType.query.filter_by(description=cp).first()
        if cp_type:
            query = query.filter(Patient.cp_id == cp_type.cp_id)

    patients = query.all()
    return jsonify([{
        "patient_id": p.patient_id,
        "age": p.age,
        "sex": p.sex,
        "cp": p.chest_pain.description if p.chest_pain else None,
        "trestbps": p.trestbps,
        "chol": p.chol,
        "fbs": p.fbs,
        "restecg": p.restecg.description if p.restecg else None,
        "thalach": p.thalach,
        "exang": p.exang,
        "oldpeak": p.oldpeak,
        "slope": p.slope.description if p.slope else None,
        "ca": p.ca,
        "thal": p.thal.description if p.thal else None,
        "heart_disease_present": p.heart_disease_present
    } for p in patients])


@patients_bp.route("/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    """Return a single patient by ID."""
    p = Patient.query.get_or_404(patient_id)
    return jsonify({
        "patient_id": p.patient_id,
        "age": p.age,
        "sex": p.sex,
        "cp": p.chest_pain.description if p.chest_pain else None,
        "trestbps": p.trestbps,
        "chol": p.chol,
        "fbs": p.fbs,
        "restecg": p.restecg.description if p.restecg else None,
        "thalach": p.thalach,
        "exang": p.exang,
        "oldpeak": p.oldpeak,
        "slope": p.slope.description if p.slope else None,
        "ca": p.ca,
        "thal": p.thal.description if p.thal else None,
        "heart_disease_present": p.heart_disease_present
    })