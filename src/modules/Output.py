from abc import abstractmethod, ABC

from rich.console import Console
from rich.table import Table

console = Console()


class Output(ABC):

    def __init__

    @abstractmethod
    def output(self, data):

    def __init__(self, top_gainers, top_losers, top_value_coin, market_cap):
        super().__init__()
        self.top_gainers = top_gainers
        self.top_losers = top_losers
        self.top_value_coin = top_value_coin
        self.market_cap = market_cap

class OutputConsole(Output):
    def output(self, data):
        table = Table(title='Топ Роста и Падения')
        table.add_column('Рост', justify='right', style='green')
        table.add_column('За 24 часа', justify='right', style='green')
        table.add_column('Падение', justify='left', style='red')
        table.add_column('За 24 часа', justify='left', style='red')
        # заполнение таблицы с переводом процентов(float) в string
        for g, l in zip(self.top_gainers, self.top_losers):
            table.add_row(g['name'], f"{g['change24percentage']:.2f}%", l['name'], f"{l['change24percentage']:.2f}%")

        console.print(table)
        console.print(f"Самый крупный по объёму торгов: [bold green]{self.top_value_coin['name']}[/bold green]")
        console.print(f'Капитал рынка: [bold green]{self.market_cap}[/bold green]')

class JsonFormatter(OutputFormatter):
    def output(self, data):
        with open('crypto_report.json', 'w', encoding='UTF8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)


class CSVFormatter(OutputFormatter):
    def output(self, data):
        with open('crypto_report.json', 'w', encoding='UTF8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)