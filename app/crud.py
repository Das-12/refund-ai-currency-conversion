from sqlalchemy.orm import Session
from .models import CurrencyConversionRate
from datetime import datetime

def save_conversion_rates(db: Session, base_currency: str, conversion_rates: dict):
    for target_currency, rate in conversion_rates.items():
        db_rate = CurrencyConversionRate(
            base_currency=base_currency,
            target_currency=target_currency,
            conversion_rate=rate,
            created_at = datetime.now().date()
        )
        db.add(db_rate)
    db.commit()
