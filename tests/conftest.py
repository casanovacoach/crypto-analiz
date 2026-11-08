import pytest
import sqlite3

from modules.analysis import GainersAnalysis, LosersAnalysis, MarketCapAnalysis, TopValueAnalysis
from modules.coin import Coin, CoinCollection
from modules.report import Report
from modules.storage import SqliteStorage


@pytest.fixture
def sqlite_connection():
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

@pytest.fixture
def sqlite_storage(sqlite_connection):
    storage = SqliteStorage(sqlite_connection)
    storage.create_tables()
    return storage

@pytest.fixture
def sqlite_db(sqlite_storage, data_coin, data_coin_second):
    storage = sqlite_storage
    storage.save({'coins': data_coin})
    storage.save({'coins': data_coin_second})
    return storage


@pytest.fixture
def report(data_coin,
           top_gainers,
           top_losers,
           market_cap,
           top_value_coin):

    return Report(data_coin, top_gainers,
                  top_losers,
                  market_cap,
                  top_value_coin)

@pytest.fixture
def bitcoin_second():
    return Coin('bitcoin', 'bit', 'BIT', 1200, 8.5, 1300, 4200)


@pytest.fixture
def ethereum_second():
    return Coin('ethereum', 'eth', 'ETH', 63, -4.5, 450, 1050)


@pytest.fixture
def dogcoin_second():
    return Coin('dogcoin', 'dog', 'DOG', 32.5, 12.4, 850, 500)

@pytest.fixture
def bitcoin():
    return Coin('bitcoin', 'bit', 'BIT', 1000, 5.658567, 1000, 3500)


@pytest.fixture
def ethereum():
    return Coin('ethereum', 'eth', 'ETH', 70,  -2.423, 395, 1111)


@pytest.fixture
def dogcoin():
    return Coin('dogcoin', 'dog', 'DOG', 25,0.80004, 700, 298)


@pytest.fixture
def data_coin(bitcoin, ethereum, dogcoin):
    collection_coins = [bitcoin, ethereum, dogcoin]
    data_coins = CoinCollection(collection_coins)
    return data_coins

@pytest.fixture
def data_coin_second(bitcoin_second, ethereum_second, dogcoin_second):
    collection_coins = [bitcoin_second, ethereum_second, dogcoin_second]
    data_coins = CoinCollection(collection_coins)
    return data_coins

@pytest.fixture
def top_gainers(data_coin):
    coins = GainersAnalysis(data_coin)
    return coins.analyze()

@pytest.fixture
def top_losers(data_coin):
    coins = LosersAnalysis(data_coin)
    return coins.analyze()

@pytest.fixture
def market_cap(data_coin):
    coins = MarketCapAnalysis(data_coin)
    return coins.analyze()


@pytest.fixture
def top_value_coin(data_coin):
    coins = TopValueAnalysis(data_coin)
    return coins.analyze()