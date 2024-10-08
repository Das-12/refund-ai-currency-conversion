from celery import Celery
from celery.schedules import crontab

celery_app = Celery('mya-app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery_app.conf.timezone = 'UTC'

celery_app.conf.beat_schedule = {
    'fetch_conversion_rates_daily': {
        'task': 'my_app.tasks.daily_update',  # The task that will be scheduled
        'schedule': crontab(hour=0, minute=0),  # Runs daily at midnight (UTC)
        'args': ['INR'],  # Argument for the task
    },
}