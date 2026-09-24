from modules.api_request import CoinGeckoRequest, CoinMarketCapRequest
from modules.analysis import GainersAnalysis, LosersAnalysis, TopValueAnalysis, MarketCapAnalysis
from modules.output import ConsoleOutput, CsvOutput, JsonOutput
from modules.report import Report

from dotenv import load_dotenv
import os

load_dotenv()

def main():

    COINGECKO_URL = 'https://api.coingecko.com/api/v3/coins/markets'

    COINGECKO_PARAMS = {'vs_currency': 'usd',
                  'order': 'market_cap_desc',
                  'per_page': 50,
                  'page': 1}


    COINMARKETCAP_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    COINMARKETCAP_PARAMS = {
        'start': 1,
        'limit': 50,
        'convert': 'USD',
        'sort': 'market_cap',
        'sort_dir': 'desc',
    }

    COIN_MARKET_API_KEY = os.getenv('COIN_MARKET_API_KEY')

    #запрос к api и возвращаем нужные поля в data

    #COIN MARKET CAP
    coin_market_cap_request = CoinMarketCapRequest(COINMARKETCAP_URL, COINMARKETCAP_PARAMS, COIN_MARKET_API_KEY)
    data_market = coin_market_cap_request.fetch_coins_data()

    # # COIN GECKO
    coin_gecko_request = CoinGeckoRequest(COINGECKO_URL, COINGECKO_PARAMS)
    data_gecko = coin_gecko_request.fetch_coins_data()

    # У двух апи разные монеты приходят, вот проверка:
    # market_key = [coin['name'] for coin in data_market]
    # gecko_key = [coin['name'] for coin in data_gecko]
    # only_market = set(market_key) - set(gecko_key)
    # only_gecko = set(gecko_key) - set(market_key)
    # print('Только CMC:', only_market)
    # print('Только CoinGecko:', only_gecko)

    # делаем анализ один раз
    top_gainers = GainersAnalysis(data_market)
    top_losers = LosersAnalysis(data_market)
    top_value_coin = TopValueAnalysis(data_market)
    market_cap = MarketCapAnalysis(data_market)

    # Создаём отчёт
    report = Report(data_market, top_gainers.analyze(), top_losers.analyze(), market_cap.analyze(), top_value_coin.analyze())

    #Ввывод:

    #таблица
    console = ConsoleOutput(report)
    console.output()

    #JSON
    json_report = JsonOutput(report)
    json_report.output()

    #CSV
    csv_report = CsvOutput(report)
    csv_report.output()

if __name__ == "__main__":
    main()


