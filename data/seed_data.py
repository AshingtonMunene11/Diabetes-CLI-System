from db.setup import Session, Base, engine
from models.patient import Patient
from models.glucose_log import GlucoseLog
from models.medication import Medication
from datetime import datetime, date
from sqlalchemy import inspect

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
inspector = inspect(engine)
print("📋 Tables created:", inspector.get_table_names())


session = Session()

patients = [
    Patient(name="Kasongo yahye", date_of_birth=date(1992, 4, 17), contact="Kasongoyahye@gmail.com"),
    Patient(name="Ndoma Sindoma", date_of_birth=date(1985, 9, 3), contact="NdomaSindoma@gmail.com"),
    Patient(name="Donald Slump", date_of_birth=date(1978, 12, 25), contact="DonaldSlump@gmail.com")
]

session.add_all(patients)
session.commit()

logs = [
    GlucoseLog(reading=110.5, timestamp=datetime(2025, 8, 26, 8, 30), patient=patients[0]),
    GlucoseLog(reading=145.2, timestamp=datetime(2025, 8, 26, 12, 45), patient=patients[0]),
    GlucoseLog(reading=98.7, timestamp=datetime(2025, 8, 26, 7, 15), patient=patients[1]),
]

session.add_all(logs)
session.commit()

medications = [
    Medication(name="Metformin", dosage="500mg twice daily", start_date=date(2025, 8, 1), patient=patients[0]),
    Medication(name="Insulin", dosage="10 units before meals", start_date=date(2025, 7, 15), patient=patients[1]),
]

session.add_all(medications)
session.commit()

session.close()
print("✅ Seed data loaded successfully.")
