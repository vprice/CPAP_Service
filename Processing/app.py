import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import requests
from apscheduler.schedulers.background import BackgroundScheduler


with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")

def get_stats():
    
    return NoContent, 200

def populate_stats():
    print("This is a periodic processing")

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