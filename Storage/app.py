import connexion
from connexion import NoContent
import yaml
import logging.config
import logging
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

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
logger.info("Connecting to DB. Hostname: %s, port: %d" %(config["hostname"] ,config["port"]))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"], 
    app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    # Create a consume on a consumer group, that only reads new messages 
    # (uncommitted messages) when the service re-starts (i.e., it doesn't 
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
    reset_offset_on_start=False,
    auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "therapy-hours": # Change this to your event type
        # Store the event1 (i.e., the payload) to the DB
            report_therapy_hours(payload)
        elif msg["type"] == "AHI-score": # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
            # Commit the new message as being read
            report_AHI_score(payload)
        consumer.commit_offsets()

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
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)

    
    