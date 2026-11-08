def test_save_in_table(data_coin, sqlite_storage ,sqlite_connection):
    sqlite_storage.save({'coins': data_coin})
    saved_coins = sqlite_connection.execute('''SELECT * FROM coin_prices''')
    rows = saved_coins.fetchall()

    bitcoin = data_coin['BIT']
    saved_bitcoin = sqlite_connection.execute('''SELECT * FROM coin_prices 
                                                   WHERE coin_id == ? ''',
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

    actual = [
        (1, 'eth', 'ethereum', 70),
        (2, 'eth', 'ethereum', 63)
    ]

    expected = [
        (snapshot_id, coin_id, coin_name, price)
        for snapshot_id, created_at, coin_id, coin_name, price in history
        ]

    assert actual == expected
    assert all(isinstance(row[1], str) for row in history)


def test_compare_snapshots(sqlite_db):
    compare = sqlite_db.compare_snapshots(1, 2)
    expected = [
        ('bit', 'bitcoin', 1000, 1200, 200),
        ('dog', 'dogcoin', 25, 32.5, 7.5),
        ('eth', 'ethereum', 70, 63, -7)
    ]
    assert compare == expected