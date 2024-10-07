from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from .services import fetch_conversion_rates
from .crud import save_conversion_rates
from .database import get_db

scheduler = BackgroundScheduler()

def daily_update(to_currency:str):
    db = next(get_db())   
    conversion_rates = fetch_conversion_rates(to_currency)
    
    if conversion_rates:
        save_conversion_rates(db, to_currency, conversion_rates)

def start_scheduler():
    scheduler.add_job(daily_update, 'interval', days=1)
    scheduler.start()
