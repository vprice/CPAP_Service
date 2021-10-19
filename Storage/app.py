import connexion
from connexion import NoContent
import yaml
import logging.config
import logging
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from therapy_hours import TherapyHours
from AHI_score import AHI_Score

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")

config = app_config["datastore"]
DB_ENGINE = create_engine(
    'mysql+pymysql://'+ config["user"] + ':' + config["password"] + '@' + config["hostname"] +
    ':' + str(config["port"]) + "/" + config["db"] 
)
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
    logger.info("Stored event therapy-hours request with a unique id of: " + body["patient_id"])
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
    logger.info("Stored event AHI-score request with a unique id of: " + body["patient_id"])
    return NoContent, 201

def get_therapy_hours(timestamp):
    """Gets new therapy hours readings after the timestamp"""

    session = DB_SESSION()

    #timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(TherapyHours).filter(TherapyHours.date_created >= timestamp)

    results = []
    for reading in readings:
        results.append(reading.to_dict())
    
    session.close()

    logger.info("Query for Therapy Hour events after %s returns %d results" %(timestamp, len(results)))
    return results, 200

def get_AHI_score(timestamp):
    """Gets new AHI score readings after the timestamp"""
    
    session = DB_SESSION()
    #timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    
    readings = session.query(AHI_Score).filter(AHI_Score.date_created >= timestamp)

    results = []
    for reading in readings:
        results.append(reading.to_dict())
    
    session.close()

    logger.info("Query for AHI score events after %s returns %d results" %(timestamp, len(results)))
    return results, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("none5561-CPAP-Readings-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)