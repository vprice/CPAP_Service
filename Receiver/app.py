import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import requests
import datetime, json
from pykafka import KafkaClient

#Functions goes here to handle endpoints

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")

def report_therapy_hours(body):
    """Receive therapy hours event"""
    logger.info("Received event <therapy-hours> request with a unique id of " + 
                body["patient_id"])
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = { "type": "therapy-hours", 
            "datetime":   
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"), 
            "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return logger.info(f"Returned information therapy hours response (id: {body['patient_id']}) with status 201")

def report_AHI_score(body):
    """Receive AHI_score event"""
    logger.info("Received event <AHI-score> request with a unique id of " + 
                body["patient_id"])
    
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = { "type": "AHI-score", 
            "datetime":   
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"), 
            "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return logger.info(f"Returned information AHI scoer response (id: {body['patient_id']}) with status 201")

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("none5561-CPAP-Readings-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)