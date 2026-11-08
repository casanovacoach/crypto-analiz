from modules.storage import SqliteStorage

import sqlite3
import pytest


def test_create_tables(sqlite_connection):
    storage = SqliteStorage(sqlite_connection)
    storage.create_tables()

    tables = sqlite_connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()

    table_names = [row[0] for row in tables]

    assert 'snapshots' in table_names
    assert 'coin_prices' in table_names


def test_create_tables_columns(sqlite_connection):
    storage = SqliteStorage(sqlite_connection)
    storage.create_tables()

    snapshots = sqlite_connection.execute(
        "PRAGMA table_info(snapshots)"
    ).fetchall()

    coin_prices = sqlite_connection.execute(
        "PRAGMA table_info(coin_prices)"
    ).fetchall()

    assert [
        (column[1], column[2], column[3], column[5])
        for column in snapshots
    ] == [
        ('snapshot_id', 'INTEGER', 0, 1),
        ('created_at', 'TEXT', 0, 0)
    ]

    assert [
        (column[1], column[2], column[3], column[5])
        for column in coin_prices
    ] == [
        ('snapshot_id', 'INTEGER', 1, 1),
        ('coin_id', 'TEXT', 1, 2),
        ('coin_name', 'TEXT', 1, 0),
        ('price', 'REAL', 1, 0)
    ]


def test_foreign_key_constraint(sqlite_connection):
    storage = SqliteStorage(sqlite_connection)
    storage.create_tables()

    with pytest.raises(sqlite3.IntegrityError):
        sqlite_connection.execute(
            '''
            INSERT INTO coin_prices
            (snapshot_id, coin_id, coin_name, price)
            VALUES (?, ?, ?, ?)
            ''',
            (999, 'eth', 'ethereum', 70)
        )


def test_save_in_table(data_coin, sqlite_storage ,sqlite_connection):
    sqlite_storage.save({'coins': data_coin})
    saved_coins = sqlite_connection.execute('''SELECT snapshot_id, coin_id, coin_name, price FROM coin_prices''')
    rows = saved_coins.fetchall()

    bitcoin = data_coin['BIT']
    saved_bitcoin = sqlite_connection.execute('''SELECT snapshot_id, coin_id, coin_name, price FROM coin_prices 
                                                   WHERE coin_id = ? ''',
                                                (bitcoin.coin_id,) ).fetchone()

    assert saved_bitcoin == (1,
                             bitcoin.coin_id,
                             bitcoin.name,
                             bitcoin.price,)

    assert len(rows) == len(data_coin)

def test_save_snapshot_created_at(mocker, sqlite_storage, data_coin):
    mock_datetime = mocker.patch("modules.storage.datetime")
    mock_datetime.now.return_value.strftime.return_value = "2026-11-08 10:00:00"

    sqlite_storage.save({'coins': data_coin})

    results = sqlite_storage.list_snapshots()

    assert results[0][1] == "2026-11-08 10:00:00"

def test_list_snapshots(sqlite_db):
    results = sqlite_db.list_snapshots()

    assert len(results) == 2
    assert results[1][0] == 1
    assert results[0][0] == 2

def test_price_change(sqlite_db, ethereum):
    history = sqlite_db.price_change(ethereum.coin_id)

    expected = [
        (1, 'eth', 'ethereum', 70),
        (2, 'eth', 'ethereum', 63)
    ]

    actual = [
        (snapshot_id, coin_id, coin_name, price)
        for snapshot_id, created_at, coin_id, coin_name, price in history
        ]

    assert actual == expected
    assert all(isinstance(row[1], str) for row in history)


def test_price_change_unknown_coin(sqlite_db):
    history = sqlite_db.price_change('unknown_coin')

    assert history == []

def test_compare_snapshots(sqlite_db):
    compare = sqlite_db.compare_snapshots(1, 2)
    expected = [
        ('bit', 'bitcoin', 1000, 1200, 200),
        ('dog', 'dogcoin', 25, 32.5, 7.5),
        ('eth', 'ethereum', 70, 63, -7)
    ]
    assert compare == expected


def test_price_change_unknown_coin(sqlite_db):
    compare = sqlite_db.compare_snapshots(100, 500)

    assert compare == []


def test_get_top_price_movers(sqlite_db):
    top_gainers, top_losers = sqlite_db.get_top_price_movers()
    expected_gainers = [
        (1, 2, 'dog', 'dogcoin', 32.5, 30.0),
        (1, 2, 'bit', 'bitcoin', 1200, 20.0),
        (1, 2, 'eth', 'ethereum', 63, -10.0)
    ]

    expected_losers = [
        (1, 2, 'eth', 'ethereum', 63, -10.0),
        (1, 2, 'bit', 'bitcoin', 1200, 20.0),
        (1, 2, 'dog', 'dogcoin', 32.5, 30.0)
    ]

    assert top_losers == expected_losers
    assert top_gainers == expected_gainers

def test_get_top_price_movers_without_two_snapshots(sqlite_storage, data_coin):
    sqlite_storage.save({'coins': data_coin})

    top_gainers, top_losers = sqlite_storage.get_top_price_movers()

    assert top_gainers == []
    assert top_losers == []