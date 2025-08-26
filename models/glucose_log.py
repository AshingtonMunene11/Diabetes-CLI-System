from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.setup import Base
from datetime import datetime

class GlucoseLog(Base):
    __tablename__ = 'glucose_logs'

    id = Column(Integer, primary_key=True)
    reading = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now) # i will switch to utcnow for production
    patient_id = Column(Integer, ForeignKey('patients.id'))

    patient = relationship("Patient", back_populates="glucose_logs")

    def __repr__(self):
        return f"<GlucoseLog(reading={self.reading}, time={self.timestamp})>"
