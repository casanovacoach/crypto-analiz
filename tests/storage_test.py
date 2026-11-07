import sqlite3


from contextlib import closing
from modules.storage import SqliteStorage

def test_save_in_table(data_coin, sqlite_storage ,sqlite_connection):
    sqlite_storage.save({'coins': data_coin})
    saved_coins = sqlite_connection.execute('''SELECT * FROM coin_prices''')

    assert len(saved_coins) == len(data_coin)