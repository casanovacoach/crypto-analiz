from rich.console import Console
from rich.table import Table
from analysis import get_top_losers, get_top_gainers

console = Console()


def gainers_losers_table(data):
    top_gainers = get_top_gainers(data)[:3]
    top_losers = get_top_losers(data)[:3]

    table = Table(title='Топ Роста и Падения')
    table.add_column('Рост', justify='right', style='green')
    table.add_column('За 24 часа', justify='right', style='green')
    table.add_column('Падение', justify='left', style='red')
    table.add_column('За 24 часа', justify='left', style='red')

    #заполнение таблицы с переводом процентов(float) в string
    for g, l in zip(top_gainers, top_losers):
        table.add_row(g['id'], f'{g['change24percentage']:.2f}%', l['id'], f'{l['change24percentage']:.2f}%')

    console.print(table)