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


