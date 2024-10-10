# celery_tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from .services import fetch_conversion_rates
from .crud import save_conversion_rates
from .database import get_db

# Celery task to fetch and save conversion rates
@shared_task
def daily_update(to_currency: str):
    print("in daily update")
    # Get the database session
    db: Session = next(get_db())
    
    # Fetch the conversion rates from the external API
    conversion_rates = fetch_conversion_rates(to_currency)
    print(conversion_rates)
    
    # If rates are fetched successfully, save them to the database
    if conversion_rates:
        save_conversion_rates(db, to_currency, conversion_rates)
    else:
        raise Exception(f"Failed to fetch conversion rates for {to_currency}")
