from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .database import get_db
from .models import CurrencyConversionRate
from .services import fetch_conversion_rates
from .crud import save_conversion_rates
from .celery_tasks import daily_update  # Import Celery task instead of the scheduler

# We no longer need to start the scheduler in the lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # No scheduling or background processes at startup

app = FastAPI(lifespan=lifespan)

# Route to manually update currency rates
@app.post("/update-rates/")
def update_currency_rates(to_currency: str, db: Session = Depends(get_db)):
    # Fetch the conversion rates from the external API
    conversion_rates = fetch_conversion_rates(to_currency)
    
    if conversion_rates:
        # Save the rates in the database
        save_conversion_rates(db, to_currency, conversion_rates)
        return {"message": "Currency rates updated successfully"}
    else:
        return {"error": "Failed to fetch data from the API"}

# Route to get all saved conversion rates from the database
@app.get("/conversion-rates/")
def get_conversion_rates(db: Session = Depends(get_db)):
    rates = db.query(CurrencyConversionRate).all()
    return rates

# Route to trigger the update asynchronously using Celery
@app.post("/async-update/")
def async_update_currency_rates(to_currency: str):
    # Trigger the Celery task asynchronously
    daily_update.apply_async(args=[to_currency])
    return {"message": "Currency update task has been triggered asynchronously"}
