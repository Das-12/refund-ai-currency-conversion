import os
from celery import Celery
from celery.schedules import crontab
from .celery_tasks import daily_update
from dotenv import load_dotenv
from .config import Settings

load_dotenv()

# USERNAME = Settings.REDIS_USERNAME
# PASSWORD = Settings.REDIS_PASSWORD

USERNAME = os.getenv('REDIS_USERNAME')
PASSWORD = os.getenv('REDIS_PASSWORD')

print(USERNAME, PASSWORD)
# Create the Celery app instance
celery_app = Celery(
    'celery_app',
    broker=f'redis://{USERNAME}:{PASSWORD}@178.128.58.228:6379/1',
    backend=f'redis://{USERNAME}:{PASSWORD}@178.128.58.228:6379/1'
)

celery_app.conf.timezone = 'Asia/Kolkata'

celery_app.conf.beat_schedule = {
    'fetch_conversion_rates_daily': {
        'task': 'app.celery_tasks.daily_update',  
        'schedule': crontab(hour=11, minute=44),  
        'args': ['INR'],  
    },
}

celery_app.conf.update()
