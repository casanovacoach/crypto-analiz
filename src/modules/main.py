from rich.console import Console
from rich.table import Table

from api_request import fetch_coins_data
from analysis import extract_coin_fields, get_top_gainers, get_top_losers, get_sum_market_cap, get_top_value_coin


def main():
    console = Console()
    data = extract_coin_fields((fetch_coins_data()))

    def gainers_loosers_table():

        top_gainers = get_top_gainers(data)[:3]
        top_losers = get_top_losers(data)[:3]

        table = Table(title='Топ Роста и Падения')
        table.add_column('Рост',justify='right',style='green')
        table.add_column('За 24 часа',justify='right',style='green')
        table.add_column('Падение',justify='left',style='red')
        table.add_column('За 24 часа',justify='left',style='red')
        for g, l in zip(top_gainers, top_losers):
            table.add_row(g['id'], f'{g['change24percentage']:.2f}%', l['id'], f'{l['change24percentage']:.2f}%')

        console.print(table)

    gainers_loosers_table()

if __name__ == "__main__":
    main()


