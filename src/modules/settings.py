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


settings = Settings()
storage = StorageType(os.getenv("STORAGE", "json"))