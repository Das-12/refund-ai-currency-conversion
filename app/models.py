from sqlalchemy import Column, String, Float, Integer, DateTime  # Import DateTime from SQLAlchemy
from .database import Base

class CurrencyConversionRate(Base):
    __tablename__ = 'currency_conversion_rates'

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    conversion_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)  

