import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "arshad"
    DB_PASSWORD: str = "KldkhhmS%23392"
    DB_PASSWORD1: str = "KldkhhmS#392"
    DB_HOST: str = "152.42.240.8"
    DB_NAME: str = "currency_conversion_service"
    DB_PORT: int = 3306

    KAFKA_BROKER_URL: str = '159.89.199.213:9092'
    KAFKA_TOPIC: str = 'gst_logging'
    KAFKA_USERNAME: str = 'arshad'
    KAFKA_PASSWORD: str = 'KldkhhmS392'

    # exchangerate_api: str  

    class Config:
        env_file = ".env"  

# Create an instance of Settings
settings = Settings()
