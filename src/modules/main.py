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


    # # Сортируем за 24 часа по убыванию
    def get_top_gainers(data_coins, n=3):
        up_change = sorted(
        data_coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=True)

        return 'Топ 3 рост за 24 часа: ', up_change[:3]


    data = extract_coin_fields((fetch_coins_data()))

    # # Сортируем за 24 часа по возрастанию
    # down_change = sorted(
    #     coins,
    #     key=lambda x: x['change24percentage'] or 0,
    #     reverse=False)
    #
    # # Самый крупный по объёму торгов СОРТ
    # volume_sort = sorted(
    #     coins,
    #     key=lambda x: x['volume'] or 0,
    #     reverse=True
    # )
    # Сумма капитализации 50ти монет.
    # sum_market_cap = sum(coin.get('market_cap', 0) for coin in coins)
    #
    # print('Топ 3 падение за 24 часа: ', down_change[:3])
    # print('Самый крупный по объёму торгов ', volume_sort[:1])
    # print('Общая капитализация 50ти монет: ', sum_market_cap)

    print(get_top_gainers(data))

if __name__ == "__main__":
    main()


