from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, Session as OrmSession
from db.setup import Base

class Medication(Base):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dosage = Column(String)
    start_date = Column(Date)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    patient = relationship("Patient", back_populates="medications")

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="ck_med_name_nonempty"),
    )

    def __repr__(self):
        return f"<Medication(name={self.name}, dosage={self.dosage})>"

    # ----- ORM helper methods -----
    @classmethod
    def create(cls, session: OrmSession, patient, name: str, dosage: str = "", start_date=None):
        instance = cls(name=name, dosage=dosage, start_date=start_date, patient=patient)
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
