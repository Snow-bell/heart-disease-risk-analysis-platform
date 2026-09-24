from flask import Blueprint, jsonify, request, current_app
import numpy as np

predict_bp = Blueprint("predict", __name__)

CP_MAP = {
    "typical angina": 1,
    "atypical angina": 2,
    "non-anginal": 3,
    "asymptomatic": 4
}

RESTECG_MAP = {
    "normal": 0,
    "st-t abnormality": 1,
    "lv hypertrophy": 2
}

SLOPE_MAP = {
    "upsloping": 1,
    "flat": 2,
    "downsloping": 3
}

THAL_MAP = {
    "normal": 3,
    "fixed defect": 6,
    "reversable defect": 7
}


@predict_bp.route("/predict", methods=["POST"])
def predict():
    """Accept patient clinical values and return heart disease risk prediction."""
    data = request.get_json()

    try:
        features = [
            int(data["age"]),
            int(data["sex"]),
            int(data["trestbps"]),
            int(data["chol"]),
            int(data["fbs"]),
            int(data["thalach"]),
            int(data["exang"]),
            float(data["oldpeak"]),
            int(data["ca"]),
            CP_MAP.get(data["cp"].lower()),
            RESTECG_MAP.get(data["restecg"].lower()),
            SLOPE_MAP.get(data["slope"].lower()),
            THAL_MAP.get(data["thal"].lower())
        ]

        if any(v is None for v in features):
            return jsonify({"error": "Invalid input value"}), 400

        model = current_app.model
        scaler = current_app.scaler

        X = np.array(features).reshape(1, -1)
        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[0]
        probability = model.predict_proba(X_scaled)[0][1]

        return jsonify({
            "heart_disease_present": int(prediction),
            "risk_probability": round(float(probability), 4),
            "risk_percentage": round(float(probability) * 100, 2)
        })

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500