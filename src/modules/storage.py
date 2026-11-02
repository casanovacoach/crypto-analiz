import json
import sqlite3

from abc import abstractmethod, ABC
from datetime import datetime


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
        with sqlite3.connect("crypto.db") as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            conn.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id INTEGER PRIMARY KEY,
                created_at TEXT 
            )
            """)

            conn.execute(
                " INSERT INTO snapshots (created_at) VALUES (?)",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))

            conn.execute("""
            CREATE TABLE IF NOT EXISTS coin_prices(
            snapshot_id INTEGER NOT NULL,
            coin_id TEXT NOT NULL,
            coin_name TEXT NOT NULL,
            price REAL NOT NULL,
            PRIMARY KEY(snapshot_id, coin_id),
            FOREIGN KEY (snapshot_id) REFERENCES snapshots(snapshot_id)
            )
            """)
            conn.close()