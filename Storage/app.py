import connexion
from connexion import NoContent
import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from therapy_hours import TherapyHours
from AHI_score import AHI_Score
import datetime

DB_ENGINE = create_engine("sqlite:///information.db")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

#Functions goes here to handle endpoints

def report_therapy_hours(body):
    """Receive therapy hours event"""
    
    session = DB_SESSION()

    therapy_hours = TherapyHours(body['patient_id'],
                                 body['device_id'],
                                 body['timestamp'],
                                 body['therapy_hours'])

    session.add(therapy_hours)
    
    session.commit()
    session.close()
    return NoContent, 201

def report_AHI_score(body):
    """Receive AHI_score event"""

    session = DB_SESSION()

    AHI_score = AHI_Score(body['patient_id'],
                         body['device_id'],
                         body['timestamp'],
                         body['AHI_score'])

    session.add(AHI_score)

    session.commit()
    session.close()
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("none5561-CPAP-Readings-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)