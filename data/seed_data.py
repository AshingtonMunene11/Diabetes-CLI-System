import os, sys
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from db.setup import Session, Base, engine
from models.patient import Patient
from models.glucose_log import GlucoseLog
from models.medication import Medication
from datetime import datetime, date
from sqlalchemy import inspect

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
inspector = inspect(engine)
print("Tables created:", inspector.get_table_names())


session = Session()

patients = [
    Patient(name="Kasongo yahye", date_of_birth=date(1999, 4, 17), contact="Kasongoyahye@gmail.com"),
    Patient(name="Ndoma Sindoma", date_of_birth=date(1985, 9, 3), contact="NdomaSindoma@gmail.com"),
    Patient(name="Kamudo Dragon", date_of_birth=date(2017, 12, 25), contact="KamudoDragon@gmail.com"),
    Patient(name="Liam Nissan", date_of_birth=date(1990, 2, 10), contact="Liamnissan@gmail.com"),
    Patient(name="Theory Henry", date_of_birth=date(2000, 6, 5), contact="TheoryHenry@gmail.com"),
]
session.add_all(patients)
session.commit()

logs = [
    GlucoseLog(reading=110.5, timestamp=datetime(2025, 1, 23, 8, 30), patient=patients[0]),
    GlucoseLog(reading=145.2, timestamp=datetime(2025, 5, 3, 12, 45), patient=patients[0]),
    # Ndoma
    GlucoseLog(reading=98.7, timestamp=datetime(2025, 8, 1, 7, 15), patient=patients[1]),
    GlucoseLog(reading=105.0, timestamp=datetime(2025, 8, 5, 18, 10), patient=patients[1]),
    # Kamudu
    GlucoseLog(reading=120.0, timestamp=datetime(2025, 7, 14, 9, 0), patient=patients[2]),
    # Liam
    GlucoseLog(reading=131.0, timestamp=datetime(2025, 8, 2, 18, 20), patient=patients[3]),
    GlucoseLog(reading=124.5, timestamp=datetime(2025, 8, 3, 8, 10), patient=patients[3]),
    # Theory
    GlucoseLog(reading=115.3, timestamp=datetime(2025, 6, 22, 7, 40), patient=patients[4]),
]
session.add_all(logs)
session.commit()

medications = [
    Medication(name="Metformin", dosage="500mg twice daily", start_date=date(2025, 1, 1), patient=patients[0]),
    Medication(name="Insulin", dosage="10 units before meals", start_date=date(2025, 2, 15), patient=patients[1]),
    Medication(name="Acarbose", dosage="50mg with meals", start_date=date(2025, 3, 20), patient=patients[2]),
    Medication(name="Glipizide", dosage="5mg daily", start_date=date(2025, 4, 10), patient=patients[3]),
    Medication(name="Pioglitazone", dosage="15mg daily", start_date=date(2025, 5, 5), patient=patients[4]),
]
session.add_all(medications)
session.commit()

session.close()
print("Seed data loaded successfully.")
