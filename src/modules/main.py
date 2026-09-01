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
    best_change = sorted(
        coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=True)

    print(coins)

    print('Топ рост за 24 часа: ', best_change[:3])

if __name__ == "__main__":
    main()


