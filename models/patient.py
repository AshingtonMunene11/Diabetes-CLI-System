from db.setup import Base
from sqlalchemy import Column, Integer, String, Date, CheckConstraint
from sqlalchemy.orm import relationship, Session as OrmSession
from datetime import date

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact = Column(String)

    glucose_logs = relationship("GlucoseLog", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="ck_patient_name_nonempty"),
    )

    # ----- Computed properties -----
    @property
    def age(self) -> int:
        if not self.date_of_birth:
            return 0
        today = date.today()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return years

    @property
    def average_glucose(self) -> float:
        if not self.glucose_logs:
            return 0.0
        total = sum(log.reading for log in self.glucose_logs)
        return round(total / len(self.glucose_logs), 2)

    # ----- ORM helper methods -----
    @classmethod
    def create(cls, session: OrmSession, name: str, date_of_birth: date, contact: str = ""):
        instance = cls(name=name, date_of_birth=date_of_birth, contact=contact)
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
    def find_by_name(cls, session: OrmSession, name: str):
        return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()

    def delete(self, session: OrmSession):
        session.delete(self)
        session.commit()
