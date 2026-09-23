import json
from abc import abstractmethod, ABC

from rich.console import Console
from rich.table import Table

console = Console()


class Output(ABC):

    def __init__(self, report):
        self.report = report

    @abstractmethod
    def output(self):
        pass


class ConsoleOutput(Output):

    def __init__(self, report):
            super().__init__(report)

    def output(self):
        table = Table(title='Топ Роста и Падения')
        table.add_column('Рост', justify='right', style='green')
        table.add_column('За 24 часа', justify='right', style='green')
        table.add_column('Падение', justify='left', style='red')
        table.add_column('За 24 часа', justify='left', style='red')
        # заполнение таблицы с переводом процентов(float) в string
        for g, l in zip(self.report.top_gainers, self.report.top_losers):
            table.add_row(g['name'], f"{g['change_24h']:.2f}%", l['name'], f"{l['change_24h']:.2f}%")

        console.print(table)
        console.print(f"Самый крупный по объёму торгов: [bold green]{self.report.highest_volume['name']}[/bold green]")
        console.print(f'Капитал рынка: [bold green]{self.report.total_market_cap_usd}[/bold green]')

class JsonOutput(Output):

    def __init__(self, report):
            super().__init__(report)

    def output(self):
        with open('crypto_report.json', 'w', encoding='UTF8') as f:
            json.dump(self.report.__dict__, f, indent=4, ensure_ascii=False)


class CsvOutput(Output):

    def __init__(self, report):
            super().__init__(report)

    def output(self):
        with open('crypto_report.json', 'w', encoding='UTF8') as f:
            json.dump(self.report, f, indent=4, ensure_ascii=False)