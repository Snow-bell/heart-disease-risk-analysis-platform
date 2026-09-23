from flask import Blueprint, jsonify
from models.lookups import ChestPainType, ThalType, RestecgType, SlopeType

lookups_bp = Blueprint("lookups", __name__)


@lookups_bp.route("/chest-pain-types")
def get_chest_pain_types():
    types = ChestPainType.query.all()
    return jsonify([{"code": t.code, "description": t.description} for t in types])


@lookups_bp.route("/thal-types")
def get_thal_types():
    types = ThalType.query.all()
    return jsonify([{"code": t.code, "description": t.description} for t in types])


@lookups_bp.route("/restecg-types")
def get_restecg_types():
    types = RestecgType.query.all()
    return jsonify([{"code": t.code, "description": t.description} for t in types])


@lookups_bp.route("/slope-types")
def get_slope_types():
    types = SlopeType.query.all()
    return jsonify([{"code": t.code, "description": t.description} for t in types])