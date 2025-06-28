import os
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # App metadata
    APP_NAME: str = "In-Store Assistant API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Inventory source
    INVENTORY_PATH: str = "./data/product_db.json"

    # NLP model settings
    NLP_MODEL: str = "en_core_web_sm"

    # Whisper model
    STT_MODEL_SIZE: str = "small"

    # Recommendation settings
    MAX_RECOMMENDATIONS: int = 5

    # Pathfinding map
    STORE_MAP_PATH: str = "./data/store_map.json"

    class Config:
        env_file = ".env"


# Singleton for app-wide config
settings = Settings()
