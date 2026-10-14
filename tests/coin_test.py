def test_top_gainers(data_coin):
    top_gainers = data_coin.top_gainers()
    assert top_gainers[0].name == 'bitcoin'


def test_top_losers(data_coin):
    top_losers = data_coin.top_losers()
    assert top_losers[0].name == 'ethereum'

def test_top_volume(data_coin):
    top_volume = data_coin.top_volume()
    assert top_volume.name == 'bitcoin'
    assert top_volume.volume == 1000

def test_total_market_cap(data_coin):
    total_market_cap = data_coin.total_market_cap()
    assert total_market_cap == 4909