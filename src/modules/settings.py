import os

from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class StorageType(Enum):
    SQLITE = 'sqlite'
    JSON = 'json'


class Settings:

    def __init__(self):
        self.storage: StorageType = StorageType(
            os.getenv("STORAGE", "json")
        )
        self.database_path = os.getenv("DATABASE_PATH", "crypto.db")


settings = Settings()