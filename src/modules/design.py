from rich.console import Console
from rich.table import Table
from modules.analysis import get_top_losers, get_top_gainers, get_top_value_coin, get_sum_market_cap

console = Console()


def gainers_losers_table(data):
    top_gainers = get_top_gainers(data)
    top_losers = get_top_losers(data)
    top_value_coin = get_top_value_coin(data)
    market_cap = get_sum_market_cap(data)
    table = Table(title='Топ Роста и Падения')
    table.add_column('Рост', justify='right', style='green')
    table.add_column('За 24 часа', justify='right', style='green')
    table.add_column('Падение', justify='left', style='red')
    table.add_column('За 24 часа', justify='left', style='red')
    #заполнение таблицы с переводом процентов(float) в string
    for g, l in zip(top_gainers, top_losers):
        table.add_row(g['name'], f"{g['change24percentage']:.2f}%", l['name'], f"{l['change24percentage']:.2f}%")

    console.print(table)
    console.print(f'Самый крупный по объёму торгов: [bold green]{top_value_coin['name']}[/bold green]')
    console.print(f'Капитал рынка: [bold green]{market_cap}[/bold green]')