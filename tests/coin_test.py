import pytest

from modules.coin import Coin, CoinCollection
def test_coin_create(bitcoin):

    assert bitcoin.name == 'bitcoin'
    assert bitcoin.symbol == 'BIT'
    assert bitcoin.change_24h == 5.658567
    assert bitcoin.volume == 1000
    assert bitcoin.market_cap == 3500

@pytest.mark.parametrize("name" , ['', ' '])
def test_coin_empty_name(name):
    with pytest.raises(ValueError):
        Coin(name, 'PIG', 11.22242, 233, 777)

def test_collection_create(ethereum, bitcoin, dogcoin):
    coins_list = [ethereum, bitcoin, dogcoin]
    collection = CoinCollection(coins_list)
    assert len(collection.coins) == len(coins_list)


def test_coin_lt(bitcoin, dogcoin):
    assert dogcoin < bitcoin


def test_coin_gt(bitcoin, dogcoin):
    assert bitcoin > dogcoin


def test_coin_repr(bitcoin):
    assert repr(bitcoin) == f'{bitcoin.name} {bitcoin.symbol} {bitcoin.change_24h:+.2f}'


def test_coin_str(bitcoin):
    assert str(bitcoin) == f'{bitcoin.name} {bitcoin.symbol} изменение за 24 часа: {bitcoin.change_24h:+.2f}%'


def test_top_gainers(data_coin):
    top_gainers = data_coin.top_gainers()
    assert top_gainers[0].name == 'bitcoin'
    assert top_gainers[2].name == 'ethereum'


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