import requests
import rich

def main():
    print("Начало программы")

    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1'

    response = requests.get(api)

    data = response.json()

    coins = []

    for coin in data:
        record = {
            'id' : coin['id'],
            'change24percentage' : coin['price_change_percentage_24h'],
            'volume' : coin['total_volume']
        }
        coins.append(record)


    # Сортируем за 24 часа по убыванию
    up_change = sorted(
        coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=True)

    # Сортируем за 24 часа по возрастанию
    down_change = sorted(
        coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=False)

    print(coins)

    print('Топ 3 рост за 24 часа: ', up_change[:3])
    print('Топ 3 падение за 24 часа: ', down_change[:3])

if __name__ == "__main__":
    main()


