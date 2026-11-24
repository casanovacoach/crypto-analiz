from modules.analysis import GainersAnalysis, LosersAnalysis, MarketCapAnalysis, TopValueAnalysis
from modules.coin import Coin, CoinCollection

import pytest
@pytest.mark.parametrize('analyze_class, expected',
                         [ (GainersAnalysis,
                              [( 'bitcoin', 5.658567),('dogcoin',0.80004)]),
                         (LosersAnalysis,
                          [('ethereum', -2.423),('dogcoin',0.80004)]
                          )]
                         )
def test_gainers_losers_analyze(data_coin,
                                analyze_class,
                                expected
                                ):

    top_coins = analyze_class(data_coin).analyze(2)

    actual = [
        (coin.name, coin.change_24h)
        for coin in top_coins
    ]
    assert actual == expected


def test_top_volume_analyze():
    dogcoin = Coin('dogcoin', 'dog', 'DOG', 700, 0.80004, 7000, 300)
    godcoin = Coin('godcoin', 'god', 'GOD', 10000, 0.01, 9000, 100)
    coins = [dogcoin, godcoin]
    collection = CoinCollection(coins)
    top_volume_coin = TopValueAnalysis(collection).analyze()
    expected = ['godcoin', 9000 ]
    actual = [top_volume_coin.name, top_volume_coin.volume]

    assert actual == expected

def test_market_cap_analyze(data_coin):
    market_cap = MarketCapAnalysis(data_coin).analyze()
    expected = 4909
    assert market_cap == expected