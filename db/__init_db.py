from db.setup import Base, engine
from models.patient import Patient
from models.glucose_log import GlucoseLog
from models.medication import Medication

Base.metadata.create_all(engine)
