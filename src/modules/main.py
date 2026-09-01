import requests
import rich

def main():
    print("Начало программы")

#    def retry(max_attemps=3, delay=2):
#        pass

    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1'

    response = requests.get(api)

    data = response.json()

    for coin in data:
        id_val = coin['id']
        change24percentage = coin['price_change_percentage_24h']
        volume = coin['total_volume']

        print(id_val, change24percentage, volume)

    print('Json row: ', data)

if __name__ == "__main__":
    main()


