import functools
import time
from abc import ABC, abstractmethod

import requests
from modules.coin import Coin
# Декоратор для повторных HTTP-запросов
def retry(max_attempts, delay):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except requests.RequestException as e:
                    last_exception = e

                    if attempt < max_attempts:
                        print(
                            f'Попытка {attempt} не удалась, '
                            f'ждём {delay} секунды, и делаем ещё попытку.'
                        )
                        time.sleep(delay)

            raise last_exception

        return wrapper

    return deco


class APIRequest(ABC):

    def __init__(self, api_url, params, session):
        self.api_url = api_url
        self.params = params
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @retry(max_attempts=3, delay=2)
    def fetch_coins_data(self):
        response = self.session.get(
            self.api_url,
            params=self.params,
            headers=self.headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return self.extract_coin_fields(data)

    @staticmethod
    @abstractmethod
    def extract_coin_fields(data):
        pass


class CoinGeckoRequest(APIRequest):


    @property
    def headers(self):
        return {}

    @staticmethod
    def extract_coin_fields(data):
        coins = []

        for coin in data:
            record = Coin(
                name=coin['name'],
                symbol=coin['symbol'],
                change_24h=coin['price_change_percentage_24h'] or 0,
                volume=coin['total_volume'] or 0,
                market_cap=coin['market_cap'] or 0,
            )

            coins.append(record)

        return coins


class CoinMarketCapRequest(APIRequest):

    def __init__(self, api_url, params, session, api_key):
        super().__init__(api_url, params, session)
        self.api_key = api_key

    @property
    def headers(self):
        return {
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }

    @staticmethod
    def extract_coin_fields(data):
        coins = []

        for coin in data['data']:
            record = Coin(
                name=coin['name'],
                symbol=coin['symbol'],
                change_24h=coin['quote']['USD']['percent_change_24h'] or 0,
                volume=coin['quote']['USD']['volume_24h'] or 0,
                market_cap=coin['quote']['USD']['market_cap'] or 0,
            )

            coins.append(record)

        return coins