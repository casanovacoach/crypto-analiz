import pytest

from modules.analysis import GainersAnalysis, LosersAnalysis, MarketCapAnalysis, TopValueAnalysis
from modules.coin import Coin, CoinCollection


@pytest.fixture
def bitcoin():
    return Coin('bitcoin', 'BIT', 5.658567, 1000, 3500)


@pytest.fixture
def ethereum():
    return Coin('ethereum', 'ETH', -2.423, 395, 1111)


@pytest.fixture
def dogcoin():
    return Coin('dogcoin', 'DOG', 0.80004, 700, 298)


@pytest.fixture
def data_coin(bitcoin, ethereum, dogcoin):
    collection_coins = [bitcoin, ethereum, dogcoin]
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