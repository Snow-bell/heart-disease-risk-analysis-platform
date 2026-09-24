import os
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

MODEL_PATH = "backend/ml/model.joblib"
SCALER_PATH = "backend/ml/scaler.joblib"

FEATURES = ["age", "sex", "trestbps", "chol", "fbs", "thalach", "exang", "oldpeak", "ca"]


def load_data():
    """Load patient data from the database into a DataFrame."""
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                age, sex, trestbps, chol, fbs, thalach, exang, oldpeak, ca,
                cpt.code AS cp,
                rt.code AS restecg,
                st.code AS slope,
                tt.code AS thal,
                CASE WHEN heart_disease_present > 0 THEN 1 ELSE 0 END AS target
            FROM patient p
            LEFT JOIN chest_pain_type cpt ON p.cp_id = cpt.cp_id
            LEFT JOIN restecg_type rt ON p.restecg_id = rt.restecg_id
            LEFT JOIN slope_type st ON p.slope_id = st.slope_id
            LEFT JOIN thal_type tt ON p.thal_id = tt.thal_id
        """), conn)
    return df


def train():
    """Train a logistic regression model and save it to disk."""
    df = load_data()
    
    all_features = FEATURES + ["cp", "restecg", "slope", "thal"]
    X = df[all_features]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Scaler saved to {SCALER_PATH}")


if __name__ == "__main__":
    train()