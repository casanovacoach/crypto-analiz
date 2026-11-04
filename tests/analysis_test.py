from modules.analysis import GainersAnalysis, LosersAnalysis, MarketCapAnalysis, TopValueAnalysis


def test_gainers_analyze(data_coin):
    top_gainers = GainersAnalysis(data_coin).analyze(2)

    expected = [
        (
            'bitcoin', 5.658567
        ),
        (
            'dogcoin',0.80004
        )
    ]
    actual = [
        (coin.name, coin.change_24h)
        for coin in top_gainers
    ]

    assert actual == expected


def test_losers_analyze(data_coin):
    top_losers = LosersAnalysis(data_coin).analyze(2)

    expected = [
        (
            'ethereum', -2.423
        ),
        (
            'dogcoin',0.80004
        )
    ]
    actual = [
        (coin.name, coin.change_24h)
        for coin in top_losers
    ]

    assert actual == expected


def test_top_volume_analyze(data_coin):
    top_volume_coin = TopValueAnalysis(data_coin).analyze()

    expected = ['bitcoin', 1000 ]
    actual = [top_volume_coin.name, top_volume_coin.volume]

    assert actual == expected

def test_market_cap_analyze(data_coin):
    market_cap = MarketCapAnalysis(data_coin).analyze()
    expected = 4909
    assert market_cap == expected