import connexion
from connexion import NoContent
import json
import os
import requests
EVENT_FILE = 'events.json' #Assume that JSON file is in the same directory and exist
MAX_EVENTS = 12

#Functions goes here to handle endpoints

"""
Keep in mind that sqlite only like to handle a single thread not multiple threads at once. Therefore,
commit/write current changes first before opening a new thread.
"""
def report_therapy_hours(body):
    """Receive therapy hours event"""
    headers = {"content-type": "application/json"}
    response = requests.post("http://localhost:8090/information/therapy-hours", json=body, headers=headers)

    
    if response.status_code == 201:
        print(response.status_code)
    else:
        print("Error: " + response.status_code)
    
    return NoContent, 201

def report_AHI_score(body):
    """Receive AHI_score event"""
    headers = {"content-type": "application/json"}
    response = requests.post("http://localhost:8090/information/AHI-score", json=body, headers=headers)

    if response.status_code == 201:
        print(response.status_code)
    else:
        print("Error: " + response.status_code)
    
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("none5561-CPAP-Readings-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)