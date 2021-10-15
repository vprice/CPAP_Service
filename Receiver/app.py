import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import requests

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
    headers = {"content-type": "application/json"}
    response = requests.post(app_config["eventstore1"]["url"], json=body, headers=headers)

    
    if response.status_code == 201:
        logger.info("Returned event <therapy-hours> response (Id: " + body["patient_id"] + ") with status code " + 
                    str(response.status_code))
    else:
        logger.info("Returned error: " + str(response.status_code))
    
    return NoContent, 201

def report_AHI_score(body):
    """Receive AHI_score event"""
    logger.info("Received event <AHI-score> request with a unique id of " + 
                body["patient_id"])
    headers = {"content-type": "application/json"}
    response = requests.post(app_config["eventstore2"]["url"], json=body, headers=headers)

    if response.status_code == 201:
        logger.info("Returned event <AHI-score> response (Id: " + body["patient_id"] + ") with status code " + 
                    str(response.status_code))
    else:
        logger.info("Returned error: " + str(response.status_code))
    
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("none5561-CPAP-Readings-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)