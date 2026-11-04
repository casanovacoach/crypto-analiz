import json
import sqlite3

from abc import abstractmethod, ABC
from datetime import datetime
from contextlib import closing


class BaseStorage(ABC):

    @abstractmethod
    def save(self, results: dict) -> None:
        pass


class JsonStorage(BaseStorage):

    def save(self, results: dict) -> None:
        with open('crypto_report.json', 'w', encoding='UTF8') as f:
            json.dump(results['report'], f, indent=4, ensure_ascii=False)

class SqliteStorage(BaseStorage):

    def create_tables(self):
        with closing(sqlite3.connect("crypto.db")) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS snapshots
                         ( snapshot_id INTEGER PRIMARY KEY,
                             created_at TEXT
                         ) """)

            conn.execute("""
                         CREATE TABLE IF NOT EXISTS coin_prices
                         (
                             snapshot_id INTEGER NOT NULL,
                             coin_id TEXT NOT NULL,
                             coin_name TEXT NOT NULL,
                             price REAL NOT NULL,
                             PRIMARY KEY ( snapshot_id, coin_id ),
                             FOREIGN KEY ( snapshot_id) REFERENCES snapshots ( snapshot_id)
                             )
                         """)

    def save(self, results: dict) -> None:

        coins = results['coins']
        rows = []

        with closing(sqlite3.connect("crypto.db")) as conn:
            with conn:

                cursor = conn.execute(
                    " INSERT INTO snapshots (created_at) VALUES (?)",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
                last_snapshot_id = cursor.lastrowid
                for coin in coins:
                    rows.append((last_snapshot_id,
                                str(coin.coin_id),
                                coin.name,
                                coin.price))

                conn.executemany("INSERT INTO coin_prices(snapshot_id, coin_id, coin_name, price) "
                             "VALUES (?, ?, ?, ?)",
                            rows)

    def price_change(self, coin_id):

        with closing(sqlite3.connect("crypto.db")) as conn:
            with conn:
                cursor = conn.execute(
                    '''SELECT s.snapshot_id, s.created_at, cp.coin_id, cp.coin_name, cp.price FROM snapshots AS s
                             JOIN coin_prices AS cp
                             ON s.snapshot_id = cp.snapshot_id
                             WHERE cp.coin_id = ?
                             ORDER BY s.snapshot_id ASC''',
                             (str(coin_id),)
                            )

                results = cursor.fetchall()

                return results