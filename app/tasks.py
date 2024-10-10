# tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from .services import fetch_conversion_rates
from .crud import save_conversion_rates
from .database import get_db

import logging
logger = logging.getLogger(__name__)

@shared_task
def daily_update(to_currency: str):
    logger.info("Starting daily update task")
    db: Session = next(get_db())
    try:
        conversion_rates = fetch_conversion_rates(to_currency)
        if conversion_rates:
            save_conversion_rates(db, to_currency, conversion_rates)
            db.commit()
            logger.info(f"Successfully updated rates for {to_currency}")
        else:
            logger.error(f"Failed to fetch rates for {to_currency}")
            raise Exception("No conversion rates found")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

