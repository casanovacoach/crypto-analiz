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
    def list_snapshots(self):
        with closing(sqlite3.connect("crypto.db")) as conn:
            results = conn.execute('''
                SELECT snapshot_id, created_at
                FROM snapshots
                ORDER BY snapshot_id DESC''').fetchall()

            return results

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


    def compare_snapshots(self, old_id, new_id):
        with closing(sqlite3.connect("crypto.db")) as conn:
            with conn:
                cursor = conn.execute(
                    '''SELECT old.coin_id, old.coin_name,
                    old.price AS old_price,
                    new.price AS new_price,
                    new.price - old.price AS price_difference
                    FROM coin_prices AS old
                    JOIN coin_prices AS new
                    ON old.coin_id = new.coin_id
                    WHERE old.snapshot_id = ?
                    AND new.snapshot_id = ?''',
                    (old_id, new_id)
                )
                results = cursor.fetchall()

                return results

    def get_top_price_movers(self):
        with closing(sqlite3.connect("crypto.db")) as conn:
            base_query = '''SELECT old.snapshot_id AS old_snapshot,
                              new.snapshot_id AS new_snapshot,
                              old.coin_id, 
                              old.coin_name,
                              new.price,
                    ROUND(((new.price - old.price) / NULLIF(old.price, 0)) * 100, 2 )
                                  AS change_percent
                    FROM coin_prices AS new
                    INNER JOIN coin_prices AS old
                        ON old.coin_id = new.coin_id
                    WHERE old.snapshot_id = (
                          SELECT snapshot_id
                          FROM snapshots
                          ORDER BY snapshot_id DESC
                          LIMIT 1 OFFSET 1)
                    AND new.snapshot_id = (
                        SELECT snapshot_id
                        FROM snapshots
                        ORDER BY snapshot_id DESC
                        LIMIT 1)
                    '''

        top_gainers = conn.execute(base_query +
                        '''ORDER BY change_percent DESC
                            LIMIT 5''').fetchall()

        top_losers = conn.execute(base_query +
                                      '''ORDER BY change_percent ASC
                                        LIMIT 5''').fetchall()

        return top_gainers, top_losers
