from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.setup import Base

class Medication(Base):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dosage = Column(String)
    start_date = Column(Date)
    patient_id = Column(Integer, ForeignKey('patients.id'))

    patient = relationship("Patient", back_populates="medications")

    def __repr__(self):
        return f"<Medication(name={self.name}, dosage={self.dosage})>"
