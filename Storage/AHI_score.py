from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import REAL, Float
from base import Base
import datetime

class AHI_Score(Base):
    #AHI Score Event

    __tablename__ = "AHI_score"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String(250), nullable=False)
    device_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    AHI_score = Column(Float, nullable=False)

    def __init__(self, patient_id, device_id, timestamp, AHI_score):
        self.patient_id = patient_id
        self.device_id = device_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.AHI_score = AHI_score

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['patient_id'] = self.patient_id
        dict['device_id'] = self.device_id
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['AHI_score'] = self.AHI_score

        return dict