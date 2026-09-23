from modules.api_request import APIRequest, API_URL, API_PARAMS
from modules.analysis import GainersAnalysis, LosersAnalysis, TopValueAnalysis, MarketCapAnalysis
from modules.output import ConsoleOutput, CsvOutput, JsonOutput
from modules.report import Report

def main():

    #запрос к api и возвращаем нужные поля в data

    request = APIRequest(API_URL, API_PARAMS)
    data_coins = request.fetch_coins_data()


    # делаем анализ один раз
    top_gainers = GainersAnalysis(data_coins)
    top_losers = LosersAnalysis(data_coins)
    top_value_coin = TopValueAnalysis(data_coins)
    market_cap = MarketCapAnalysis(data_coins)

    # Создаём отчёт
    report = Report(data_coins, top_gainers.analyze(), top_losers.analyze(), market_cap.analyze(), top_value_coin.analyze())

    #Ввывод:

    # #таблица
    console = ConsoleOutput(report)
    console.output()

if __name__ == "__main__":
    main()


