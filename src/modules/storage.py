import json
import sqlite3

from abc import abstractmethod, ABC


class BaseStorage(ABC):

    @abstractmethod
    def save(self, results: dict) -> None:
        pass


class JsonStorage(BaseStorage):

    def save(self, results: dict) -> None:
        with open('crypto_report.json', 'w', encoding='UTF8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

class SqliteStorage(BaseStorage):

    def save(self, results: dict) -> None:
        pass