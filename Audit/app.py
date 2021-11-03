from yaml import events
import connexion
import yaml
import logging, logging.config
from connexion import NoContent
import requests
import datetime, json
from pykafka import KafkaClient

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")

def get_therapy_hours(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue. 
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)

    logger.info("Retrieving therapy hours at index %d" % index)
    therapy_hours_events= []
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            # Find the event at the index you want and 
            # return code 200
            # i.e., return event, 200
            if msg['type'] == 'therapy-hours': 
                therapy_hours_events.append(msg)
                
        print("Therapy Hour Events:", len(therapy_hours_events))

        if index < len(therapy_hours_events):
            return therapy_hours_events[index], 200
    except: 
        logger.error("No more messages found")

    logger.error("Could not find therapy hours at index %d" % index)
    return { "message": "Not Found"}, 404

def get_AHI_score(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue. 
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)

    logger.info("Retrieving AHI score at index %d" % index)
    AHI_score_events= []
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            # Find the event at the index you want and 
            # return code 200
            # i.e., return event, 200
            if msg['type'] == 'therapy-hours': 
                AHI_score_events.append(msg)
                
        print("Therapy Hour Events:", len(AHI_score_events))

        if index < len(AHI_score_events):
            return AHI_score_events[index], 200

    except: 
        logger.error("No more messages found")

    logger.error("Could not find temperature at index %d" % index)
    return { "message": "Not Found"}, 404
