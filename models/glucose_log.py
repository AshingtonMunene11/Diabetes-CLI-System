from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, Session as OrmSession
from db.setup import Base
from datetime import datetime

class GlucoseLog(Base):
    __tablename__ = 'glucose_logs'

    id = Column(Integer, primary_key=True)
    reading = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    patient = relationship("Patient", back_populates="glucose_logs")

    __table_args__ = (
        CheckConstraint("reading > 0", name="ck_glucose_reading_positive"),
    )

    def __repr__(self):
        return f"<GlucoseLog(reading={self.reading}, time={self.timestamp})>"

    # ----- ORM helper methods -----
    @classmethod
    def create(cls, session: OrmSession, patient, reading: float, timestamp: datetime = None):
        instance = cls(reading=reading, timestamp=timestamp or datetime.now(), patient=patient)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def get_by_id(cls, session: OrmSession, id_: int):
        return session.get(cls, id_)

    @classmethod
    def get_all(cls, session: OrmSession):
        return session.query(cls).all()

    @classmethod
    def find_by_date_range(cls, session: OrmSession, start: datetime, end: datetime):
        return session.query(cls).filter(cls.timestamp.between(start, end)).all()

    def delete(self, session: OrmSession):
        session.delete(self)
        session.commit()
