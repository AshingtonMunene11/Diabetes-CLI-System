from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from db.setup import Base

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact = Column(String) #email or phone number, REMEMBER need to validate this eventually`

    glucose_logs = relationship("GlucoseLog", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(name={self.name}, DOB={self.date_of_birth})>"
