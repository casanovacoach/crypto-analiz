from modules.api_request import fetch_coins_data
from modules.analysis import extract_coin_fields, get_top_gainers, get_top_losers, get_top_value_coin, get_sum_market_cap
from modules.design import gainers_losers_table, console
from modules.report import report_generator

def main():


    #запрос к api и возвращаем нужные поля в data
    with console.status('Загрузка данных...'):
        data = extract_coin_fields(fetch_coins_data())

    # делаем анализ один раз
    top_gainers = get_top_gainers(data)
    top_losers = get_top_losers(data)
    top_value_coin = get_top_value_coin(data)
    market_cap = get_sum_market_cap(data)

    #Таблица
    gainers_losers_table(top_gainers, top_losers, top_value_coin, market_cap)

    #Создаём отчёт
    report_generator(data, top_gainers, top_losers, market_cap, top_value_coin)

if __name__ == "__main__":
    main()


