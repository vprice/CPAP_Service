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
EVENT_FILE = 'events.json' #Assume that JSON file is in the same directory and exist
MAX_EVENTS = 12

DB_ENGINE = create_engine("sqlite:///information.db")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

#Functions goes here to handle endpoints
"""
def log_json_file(body):
    event_list = []
    with open(EVENT_FILE, 'r') as open_file:
        if os.stat(EVENT_FILE).st_size == 0: #File is empty
            event_list.append(body)
        else:
            event_list = json.load(open_file)
            if(len(event_list) >= MAX_EVENTS):
                event_list.pop(0)
            event_list.append(body)
    with open(EVENT_FILE, 'w') as open_file:
        json.dump(event_list, open_file, indent = 4, sort_keys=True)
"""

def report_therapy_hours(body):
    """Receive therapy hours event"""
    
    #log_json_file(body)
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

    #log_json_file(body)
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