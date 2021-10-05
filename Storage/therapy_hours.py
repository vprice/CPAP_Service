from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import REAL, Float
from base import Base
import datetime

class TherapyHours(Base):
    #Therapy Hours Event

    __tablename__ = "therapy_hours"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String(250), nullable=False)
    device_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    therapy_hours = Column(Float, nullable=False)

    def __init__(self, patient_id, device_id, timestamp, therapy_hours):
        self.patient_id = patient_id
        self.device_id = device_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.therapy_hours = therapy_hours

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['patient_id'] = self.patient_id
        dict['device_id'] = self.device_id
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['therapy_hours'] = self.therapy_hours

        return dict
