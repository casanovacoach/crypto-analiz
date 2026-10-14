from modules.analysis import GainersAnalysis, LosersAnalysis, MarketCapAnalysis, TopValueAnalysis
from modules.coin import Coin, CoinCollection

import pytest

@pytest.fixture
def data_coin():
    ethereum = Coin('ethereum', 'ETH', -2.423, 395, 1111)
    bitcoin = Coin('bitcoin', 'BIT', 5.658567, 1000, 3500)
    dogcoin = Coin('dogcoin', 'DOG', 0.80004, 700, 298)
    print(ethereum)

    collection_coins = [bitcoin, ethereum, dogcoin]
    data_coins = CoinCollection(collection_coins)
    print('дата коин: ', type(data_coins))
    print(data_coins.__dict__)
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