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

# Set the timezone to IST (Indian Standard Time)
celery_app.conf.timezone = 'Asia/Kolkata'

# Define the periodic task schedule
celery_app.conf.beat_schedule = {
    'fetch_conversion_rates_daily': {
        'task': 'app.celery_tasks.daily_update',  # Ensure this matches the task path
        'schedule': crontab(hour=12, minute=31),  # Runs daily at 7:35 PM IST (Asia/Kolkata timezone)
        'args': ['INR'],  # Arguments to pass to the task
    },
}

# Update the app configuration if needed (this is optional)
celery_app.conf.update()
