

from api_request import fetch_coins_data
from analysis import extract_coin_fields, get_top_gainers, get_top_losers, get_sum_market_cap, get_top_value_coin
from design import gainers_losers_table, console

def main():

    with console.status('Загрузка данных...'):
        data = extract_coin_fields((fetch_coins_data()))

    gainers_losers_table(data)

if __name__ == "__main__":
    main()


