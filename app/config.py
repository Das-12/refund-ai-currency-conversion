# import os
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DB_USER: str = "arshad"
#     DB_PASSWORD: str = "KldkhhmS%23392"
#     DB_PASSWORD1: str = "KldkhhmS#392"
#     DB_HOST: str = "152.42.240.8"
#     DB_NAME: str = "currency_conversion_service"
#     DB_PORT: int = 3306

#     KAFKA_BROKER_URL: str = '159.89.199.213:9092'
#     KAFKA_TOPIC: str = 'gst_logging'
#     KAFKA_USERNAME: str = 'arshad'
#     KAFKA_PASSWORD: str = 'KldkhhmS392'

#     # exchangerate_api: str 
#     REDIS_USERNAME: str = "default"
#     REDIS_HOST: str = "178.128.58.228"
#     REDIS_PORT:int = 6379
#     REDIS_PASSWORD: str = "KldkhhmS392"
#     REDIS_DB:int = 1


#     class Config:
#         env_file = ".env"  

# # Create an instance of Settings
# settings = Settings()

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = os.getenv("DB_USER", "arshad")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "KldkhhmS%23392")
    DB_PASSWORD1: str = os.getenv("DB_PASSWORD1", "KldkhhmS#392")  
    DB_HOST: str = os.getenv("DB_HOST", "152.42.240.8")
    DB_NAME: str = os.getenv("DB_NAME", "currency_conversion_service")
    DB_PORT: int = os.getenv("DB_PORT", 3306)

    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL", '159.89.199.213:9092')
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", 'gst_logging')
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME", 'arshad')
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD", 'KldkhhmS392')

    REDIS_USERNAME: str = os.getenv("REDIS_USERNAME", "default")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "178.128.58.228")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "KldkhhmS392")
    REDIS_DB: int = os.getenv("REDIS_DB", 1)

    class Config:
        env_file = ".env" 
        extra = "forbid"    


settings = Settings()



