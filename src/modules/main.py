from api_request import fetch_coins_data
from analysis import extract_coin_fields, get_top_gainers, get_top_loosers, get_sum_market_cap, get_top_value_coin


def main():

    data = extract_coin_fields((fetch_coins_data()))
    print(get_top_gainers(data))

if __name__ == "__main__":
    main()


