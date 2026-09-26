from flask import Flask
from flask_cors import CORS
from models.base import db
from config import Config
from routes.patients import patients_bp
from routes.stats import stats_bp
from routes.lookups import lookups_bp
from routes.predict import predict_bp
import joblib
import os

def create_app():
    """Flask application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    # Load ML model and scaler once at startup
    app.model = joblib.load(os.getenv("MODEL_PATH", "ml/model.joblib"))
    app.scaler = joblib.load(os.getenv("SCALER_PATH", "ml/scaler.joblib"))

    app.register_blueprint(patients_bp, url_prefix="/api/patients")
    app.register_blueprint(stats_bp, url_prefix="/api/stats")
    app.register_blueprint(lookups_bp, url_prefix="/api/lookups")
    app.register_blueprint(predict_bp, url_prefix="/api")

    @app.route("/api/health")
    def health():
        """Health check endpoint."""
        return {"status": "ok"}

    return app