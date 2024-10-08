# tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from .services import fetch_conversion_rates
from .crud import save_conversion_rates
from .database import get_db

# Define a Celery task for updating conversion rates
@shared_task
def daily_update(to_currency: str):
    db: Session = next(get_db())  # Get a session from the database
    conversion_rates = fetch_conversion_rates(to_currency)
    
    if conversion_rates:
        save_conversion_rates(db, to_currency, conversion_rates)
