import functools

import requests
from pydantic import decorator
from rich.console import Console
import time

def main():

    print("Начало программы")

    def retry(max_attempts=3, delay = 2):
        def deco(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except requests.RequestException as e:
                        last_exception = e
                        if attempt == max_attempts:
                            break
                        print(f'Попытка {attempt} не удалась, ждём {delay}, и делаем ещё попытку.')
                        time.sleep(delay)
                raise last_exception
            return wrapper
        return deco

    @retry(max_attempts=3, delay=2)
    def fetch_coins_data():
        api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1'
        response = requests.get(api)
        return response.json()

    # Создаём список словарей: имя монеты, изменения за 24ч, объём, капитализация
    def extract_coin_fields(data):
        coins = []
        for coin in data:
            record = {
                'id' : coin['id'],
                'change24percentage' : coin['price_change_percentage_24h'],
                'volume' : coin['total_volume'],
                'market_cap' : coin['market_cap']
            }
            coins.append(record)
        return coins


    # Сортируем за 24 часа по убыванию
    def get_top_gainers(data_coins, n=3):
        up_change = sorted(
        data_coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=True)

        return 'Топ 3 рост за 24 часа: ', up_change[:n]


    # Сортируем за 24 часа по возрастанию
    def get_down_gainers(data_coins, n=3):
        down_change = sorted(
        data_coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=False)
        return 'Топ 3 падение за 24 часа: ', down_change[:n]


    # Самый крупный по объёму торгов СОРТ
    def get_top_value_coin(data_coins, n=1):
        volume_sort = sorted(
        data_coins,
        key=lambda x: x['volume'] or 0,
        reverse=True)
        return 'Топ по объёму торгов ', data_coins[:n]

    # Сумма капитализации 50ти монет.
    def get_sum_market_cap(data_coins):
        sum_market_cap = sum(coin.get('market_cap', 0) for coin in data_coins)
        return sum_market_cap


    data = extract_coin_fields((fetch_coins_data()))

    print(get_sum_market_cap(data))

if __name__ == "__main__":
    main()


