import csv
import argparse
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}

CSV_FILE = "data/heart_disease_uci.csv"

def get_connection():
    """Establish and return a connection to the PostgreSQL database using environment variables."""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    return conn


def create_tables(conn):
    """Create lookup tables and patient table if they do not already exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chest_pain_type (
                cp_id SERIAL PRIMARY KEY,
                code INTEGER NOT NULL UNIQUE,
                description TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS thal_type (
                thal_id SERIAL PRIMARY KEY,
                code INTEGER NOT NULL UNIQUE,
                description TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS restecg_type (
                restecg_id SERIAL PRIMARY KEY,
                code INTEGER NOT NULL UNIQUE,
                description TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS slope_type (
                slope_id SERIAL PRIMARY KEY,
                code INTEGER NOT NULL UNIQUE,
                description TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS patient (
                patient_id SERIAL PRIMARY KEY,
                age INTEGER NOT NULL,
                sex INTEGER NOT NULL,
                cp_id INTEGER REFERENCES chest_pain_type(cp_id),
                trestbps INTEGER,
                chol INTEGER,
                fbs INTEGER,
                restecg_id INTEGER REFERENCES restecg_type(restecg_id),
                thalach INTEGER,
                exang INTEGER,
                oldpeak FLOAT,
                slope_id INTEGER REFERENCES slope_type(slope_id),
                ca INTEGER,
                thal_id INTEGER REFERENCES thal_type(thal_id),
                heart_disease_present INTEGER NOT NULL
            );
        """)
    conn.commit()

def create_view(conn):
    """Create a flat view of the patient table joining all lookup tables for easy querying."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE OR REPLACE VIEW patient_flat AS
            SELECT
                p.patient_id,
                p.age,
                p.sex,
                cpt.code AS cp,
                cpt.description AS cp_description,
                p.trestbps,
                p.chol,
                p.fbs,
                rt.code AS restecg,
                rt.description AS restecg_description,
                p.thalach,
                p.exang,
                p.oldpeak,
                st.code AS slope,
                st.description AS slope_description,
                p.ca,
                tt.code AS thal,
                tt.description AS thal_description,
                p.heart_disease_present
            FROM patient p
            LEFT JOIN chest_pain_type cpt ON p.cp_id = cpt.cp_id
            LEFT JOIN restecg_type rt ON p.restecg_id = rt.restecg_id
            LEFT JOIN slope_type st ON p.slope_id = st.slope_id
            LEFT JOIN thal_type tt ON p.thal_id = tt.thal_id;
        """)
    conn.commit()

def seed_lookup_tables(conn):
    """Seed lookup tables from seed.sql, skipping if already populated."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM chest_pain_type;")
        if cur.fetchone()[0] > 0:
            print("Lookup tables already seeded, skipping.")
            return

        with open("data/seed.sql", "r") as f:
            seed_sql = f.read()
        cur.execute(seed_sql)
    conn.commit()
    print("Lookup tables seeded successfully.")

def load_csv(conn):
    """Check if the patient table already has data."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM patient;")
        return cur.fetchone()[0] > 0


def is_populated(conn):
    """Load patient records from the heart disease CSV into the patient table."""
    with conn.cursor() as cur:
        # Truncate patient table before loading
        cur.execute("TRUNCATE TABLE patient RESTART IDENTITY CASCADE;")

        with open(CSV_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip rows with missing values
                if any(v == "?" or v == "" for v in row.values()):
                    continue

                # Lookup foreign keys
                cur.execute("SELECT cp_id FROM chest_pain_type WHERE description = %s", (row["cp"].lower(),))
                cp_id = cur.fetchone()
                cp_id = cp_id[0] if cp_id else None

                cur.execute("SELECT restecg_id FROM restecg_type WHERE description = %s", (row["restecg"].lower(),))
                restecg_id = cur.fetchone()
                restecg_id = restecg_id[0] if restecg_id else None

                cur.execute("SELECT slope_id FROM slope_type WHERE description = %s", (row["slope"].lower(),))
                slope_id = cur.fetchone()
                slope_id = slope_id[0] if slope_id else None

                cur.execute("SELECT thal_id FROM thal_type WHERE description = %s", (row["thal"].lower(),))
                thal_id = cur.fetchone()
                thal_id = thal_id[0] if thal_id else None

                cur.execute("""
                    INSERT INTO patient (
                        age, sex, cp_id, trestbps, chol, fbs,
                        restecg_id, thalach, exang, oldpeak,
                        slope_id, ca, thal_id, heart_disease_present
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(row["age"]),
                    int(row["sex"] == "Male"),          # convert Male/Female to 1/0
                    cp_id,
                    int(float(row["trestbps"])),
                    int(float(row["chol"])),
                    int(row["fbs"] == "TRUE"),          # convert TRUE/FALSE to 1/0
                    restecg_id,
                    int(float(row["thalch"])),          
                    int(row["exang"] == "TRUE"),        # convert TRUE/FALSE to 1/0
                    float(row["oldpeak"]),
                    slope_id,
                    int(float(row["ca"])),
                    thal_id,
                    int(float(row["num"]))
                ))
    conn.commit()
    print("Patient data loaded successfully.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Force reload data")
    args = parser.parse_args()

    conn = get_connection()

    create_tables(conn)
    create_view(conn)

    if args.force:
        print("Force flag set, reloading data...")
        seed_lookup_tables(conn)
        load_csv(conn)
    elif is_populated(conn):
        print("Database already populated, skipping load.")
    else:
        seed_lookup_tables(conn)
        load_csv(conn)

    conn.close()

if __name__ == "__main__":
    main()