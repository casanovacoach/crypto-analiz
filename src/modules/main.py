import os
import requests
import typer

from typing import Annotated
from dotenv import load_dotenv

from modules.api_request import CoinGeckoRequest, CoinMarketCapRequest
from modules.analysis import (
    GainersAnalysis,
    LosersAnalysis,
    TopValueAnalysis,
    MarketCapAnalysis,
)
from modules.coin import CoinCollection
from modules.output import ConsoleOutput, CsvOutput, JsonOutput

from modules.factory import ProviderFactory, OutputFactory, StorageFactory
from modules.report import Report
from modules.typer_option import Source, OutputFormat
from modules.settings import Settings, StorageType
from modules.storage import JsonStorage, SqliteStorage

load_dotenv()

app = typer.Typer()

settings = Settings()

storage_factories = {
    StorageType.JSON: JsonStorage,
    StorageType.SQLITE: lambda: SqliteStorage(settings.database_path),
}

storage_factory = StorageFactory(storage_factories)

@app.command()
def main(
    source: Annotated[Source, typer.Option()],
    output: Annotated[OutputFormat, typer.Option()],
    top: Annotated[int, typer.Option()] = 3
):
    COINGECKO_URL = 'https://api.coingecko.com/api/v3/coins/markets'

    COINGECKO_PARAMS = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
    }

    COINMARKETCAP_URL = (
        'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    )

    COINMARKETCAP_PARAMS = {
        'start': 1,
        'limit': 50,
        'convert': 'USD',
        'sort': 'market_cap',
        'sort_dir': 'desc',
    }

    COIN_MARKET_API_KEY = os.getenv('COIN_MARKET_API_KEY')

    session = requests.Session()

    provider_factories = {
        Source.COINGECKO: lambda: CoinGeckoRequest(
            COINGECKO_URL,
            COINGECKO_PARAMS,
            session,
        ),

        Source.COINMARKETCAP: lambda: CoinMarketCapRequest(
            COINMARKETCAP_URL,
            COINMARKETCAP_PARAMS,
            session,
            COIN_MARKET_API_KEY,
        ),
    }

    provider_factory = ProviderFactory(provider_factories)
    provider = provider_factory.create(source)

    with provider:
        coins = provider.fetch_coins_data()

    collection = CoinCollection(coins)

    top_gainers = GainersAnalysis(collection)
    top_losers = LosersAnalysis(collection)
    top_value_coin = TopValueAnalysis(collection)
    market_cap = MarketCapAnalysis(collection)

    report = Report(
        collection,
        top_gainers.analyze(top),
        top_losers.analyze(top),
        market_cap.analyze(),
        top_value_coin.analyze(),
    )

    output_factories = {
        OutputFormat.CONSOLE: lambda: ConsoleOutput(report),
        OutputFormat.JSON: lambda: JsonOutput(report),
        OutputFormat.CSV: lambda: CsvOutput(report),
    }

    output_factory = OutputFactory(output_factories)
    output_handler = output_factory.create(output)

    output_handler.output()


    storage_data = {
        "report" : report.__dict__,
        "coins" : collection.coins
    }

    with storage_factory.create(settings.storage) as storage:
        storage.save(storage_data)

@app.command("list-snapshots")
def list_snapshots_command():
    with storage_factory.create(StorageType.SQLITE) as storage:
        snapshots = storage.list_snapshots()

        if not snapshots:
            typer.echo("Снимки пока не сохранены.")
            return

        for snapshot_id, created_at in snapshots:
            typer.echo(f'{snapshot_id} | {created_at}')

@app.command("compare-snapshots")
def compare_snapshot_command(
        old_id: Annotated[int, typer.Argument()],
        new_id: Annotated[int, typer.Argument()]
):
    with storage_factory.create(StorageType.SQLITE) as storage:
        results = storage.compare_snapshots(old_id, new_id)

        if not results:
            typer.echo("Нет данных для сравнения")
            return

        typer.echo(f'Сравнение снимков {old_id}, и {new_id}:')

        for coin_id, coin_name, old_price, new_price, price_difference in results:
            typer.echo(
                f"{coin_name} ({coin_id}): "
                f"{old_price} -> {new_price} "
                f"({price_difference:+})"
            )
if __name__ == "__main__":
    app()