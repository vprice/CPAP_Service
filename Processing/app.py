from genericpath import isfile
import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import requests
import json
import os

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")

STAT_FILE = app_config["datastore"]["filename"]

def get_stats(): #Assume file not empty and has correct format
    logger.info("Get_stats() request started...")
    if(os.path.isfile('./'+STAT_FILE)):
        with open(STAT_FILE, 'r') as open_file:
            stats = json.load(open_file)
            logger.debug("Contents:"+str(stats))
            logger.info("Request Complete")
        return stats, 200
    else: #File does not exist
        logger.error("File does not exist")
        return "Statistics do not exist", 404

def populate_stats(): #Assume file not empty and has correct format
    """Periodically update stats"""
    """
    - Request each event
    - import current json object
    - iterate through each json and update json object for the latest stats 
    - write/dump json in file
    """
    logger.info("Periodic Processing has started")
    stats = { #Default Values for example
        "max_AHI_score_reading": 0,
        "max_therapy_hour_reading": 2.6,
        "num_AHI_score_readings": 0,
        "num_therapy_hour_readings": 4
    }

    if(os.path.isfile('./'+STAT_FILE)): #File exists then open it
        with open(STAT_FILE, 'r') as open_file: #Assume correct format
            stats = json.load(open_file)
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") #pass as the timestamp parameter in runtime

            #update therapy hour stats
            response_therapy_hours = requests.get(app_config["eventstore1"]["url"], params="timestamp=2016-07-29T09:12:33.001Z")#Test time is "2016-07-29T09:12:33.001Z"
            if(response_therapy_hours.status_code != 200):
                logger.error("Returned error: " + str(response_therapy_hours.status_code))
            else: 
                logger.info("Received therapy hour events:" + str(len(response_therapy_hours.json())))
            stats["num_therapy_hour_readings"] = len(response_therapy_hours.json())
            stats['max_therapy_hour_reading'] = 0
            for i in response_therapy_hours.json():
                if stats['max_therapy_hour_reading'] < i["therapy_hours"]:
                    stats['max_therapy_hour_reading'] = i["therapy_hours"] #change value to largest therapy hour reading

            #Update AHI score stats
            response_AHI_score = requests.get(app_config["eventstore2"]["url"], params="timestamp="+current_time)
            if(response_AHI_score.status_code != 200):
                logger.error("Returned error: " + str(response_AHI_score.status_code))
            else: 
                logger.info("Received therapy hour events:" + str(len(response_AHI_score.json())))
            stats["num_AHI_score_readings"] = len(response_AHI_score.json())
            stats["max_AHI_score_reading"] = 0
            for i in response_AHI_score.json():
                if stats["max_AHI_score_reading"] < i["AHI_score"]:
                    stats["max_AHI_score_reading"]= i["AHI_score"]
            
            logger.debug(stats)
    
    #Put in json file the updated stats
    with open(STAT_FILE, 'w') as open_file:
        json.dump(stats, open_file, indent=4, sort_keys=True)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("none5561-CPAP-Readings-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)