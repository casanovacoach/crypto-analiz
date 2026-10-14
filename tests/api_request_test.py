from modules.api_request import APIRequest, CoinGeckoRequest, CoinMarketCapRequest

import pytest
import requests


def test_fetch_coins_data(mocker):
    session_mock = mocker.Mock()
    response_mock = mocker.Mock()

    coin = {    'name' : 'bitcoin',
                'symbol' : 'BTS',
                'price_change_percentage_24h' : 5.0,
                'total_volume' : 71000,
                'market_cap' : '900000'}

    session_mock.get.return_value = response_mock
    response_mock.json.return_value = [coin]


    request = CoinGeckoRequest('https://coinexample.com/', {}, session=session_mock)

    coins_fake = request.fetch_coins_data()


    session_mock.get.assert_called_once_with('https://coinexample.com/',
                                             params={},
                                             headers={},
                                             timeout=10)

    assert coins_fake[0].name == 'bitcoin'
    assert coins_fake[0].volume == 71000
    assert coins_fake[0].change_24h == 5.0


def test_request_retry_decorator(mocker):
    session_mock = mocker.Mock()
    response_mock = mocker.Mock()

    session_mock.get.side_effect = requests.exceptions.RequestException
    sleep_mock = mocker.patch('modules.api_request.time.sleep')
    response_mock.json.return_value = {}

    coin_obj = CoinGeckoRequest('https://coinexample.com/', {}, session=session_mock)

    with pytest.raises(requests.RequestException):
        coin_obj.fetch_coins_data()

    assert session_mock.get.call_count == 3
    assert sleep_mock.call_count == 2