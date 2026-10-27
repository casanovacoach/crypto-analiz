from modules.api_request import CoinGeckoRequest, CoinMarketCapRequest

import pytest
import requests


def test_fetch_coins_data_gecko(mocker):
    session_mock = mocker.Mock()
    response_mock = mocker.Mock()

    coin = {    'name' : 'bitcoin',
                'symbol' : 'BTS',
                'price_change_percentage_24h' : 5.0,
                'total_volume' : 71000,
                'market_cap' : 900000
            }

    session_mock.get.return_value = response_mock
    response_mock.json.return_value = [coin]

    request = CoinGeckoRequest('https://coinexample.com/', {}, session=session_mock)

    coins_fake_gecko = request.fetch_coins_data()

    session_mock.get.assert_called_once_with('https://coinexample.com/',
                                             params={},
                                             headers={},
                                             timeout=10)

    assert coins_fake_gecko[0].name == 'bitcoin'
    assert coins_fake_gecko[0].volume == 71000
    assert coins_fake_gecko[0].change_24h == 5.0

def test_fetch_coins_data_market_cap(mocker):
    session_mock = mocker.Mock()
    response_mock = mocker.Mock()

    api_fake = 'Api'

    coin = {
        'name': 'bitcoin',
        'symbol': 'BTS',
        'quote': {
            'USD': {
                'percent_change_24h': 5.0,
                'volume_24h': None,
                'market_cap': 900000
            }
        }
    }


    session_mock.get.return_value = response_mock
    response_mock.json.return_value = {
        'data': [coin]
    }

    request_market_cap = CoinMarketCapRequest('https://coinexample.com/', {}, session=session_mock, api_key=api_fake)

    coins_fake_market_cap = request_market_cap.fetch_coins_data()

    session_mock.get.assert_called_once_with('https://coinexample.com/',
                                             params={},
                                             headers={'X-CMC_PRO_API_KEY': api_fake,
                                                      "Accept": "application/json",},
                                             timeout=10)

    assert coins_fake_market_cap[0].name == 'bitcoin'
    assert coins_fake_market_cap[0].volume == 0
    assert coins_fake_market_cap[0].change_24h == 5.0


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