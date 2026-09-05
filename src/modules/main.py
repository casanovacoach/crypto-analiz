from api_request import fetch_coins_data
from analysis import extract_coin_fields, get_top_gainers, get_top_losers, get_sum_market_cap, get_top_value_coin
from design import gainers_losers_table, console
from  report import report_generator
def main():

    #запрос к api и возвращаем нужные поля в data
    with console.status('Загрузка данных...'):
        data = extract_coin_fields((fetch_coins_data()))

    print('Джисон с нужными полями: ', data)

    #Таблица
    gainers_losers_table(data)

    #Создаём отчёт
    report_generator(data)

if __name__ == "__main__":
    main()


