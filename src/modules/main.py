from modules.api_request import CoinGeckoRequest, CoinMarketCapRequest
from modules.analysis import (
    GainersAnalysis,
    LosersAnalysis,
    TopValueAnalysis,
    MarketCapAnalysis,
)
from modules.output import ConsoleOutput, CsvOutput, JsonOutput
from modules.report import Report
from modules.factory import ProviderFactory, OutputFactory
from modules.types import Source, OutputFormat

from dotenv import load_dotenv
import os

import typer
from typing import Annotated

load_dotenv()

app = typer.Typer()


@app.command()
def main(
    source: Annotated[Source, typer.Option()],
    output: Annotated[OutputFormat, typer.Option()],
    top: Annotated[int, typer.Option()] = 3,
):
    # -------------------------
    # Конфигурация API
    # -------------------------

    COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

    COINGECKO_PARAMS = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
    }

    COINMARKETCAP_URL = (
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    )

    COINMARKETCAP_PARAMS = {
        "start": 1,
        "limit": 50,
        "convert": "USD",
        "sort": "market_cap",
        "sort_dir": "desc",
    }

    COIN_MARKET_API_KEY = os.getenv("COIN_MARKET_API_KEY")

    # -------------------------
    # Провайдеры
    # -------------------------

    provider_factories = {
        Source.COINGECKO: lambda: CoinGeckoRequest(
            COINGECKO_URL,
            COINGECKO_PARAMS,
        ),
        Source.COINMARKETCAP: lambda: CoinMarketCapRequest(
            COINMARKETCAP_URL,
            COINMARKETCAP_PARAMS,
            COIN_MARKET_API_KEY,
        ),
    }

    provider_factory = ProviderFactory(provider_factories)
    provider = provider_factory.create(source)

    # Получаем данные только от выбранного провайдера
    data = provider.fetch_coins_data()

    # -------------------------
    # Анализ
    # -------------------------

    top_gainers = GainersAnalysis(data)
    top_losers = LosersAnalysis(data)
    top_value_coin = TopValueAnalysis(data)
    market_cap = MarketCapAnalysis(data)

    # -------------------------
    # Отчёт
    # -------------------------

    report = Report(
        data,
        top_gainers.analyze(top),
        top_losers.analyze(top),
        market_cap.analyze(),
        top_value_coin.analyze(),
    )

    # -------------------------
    # Вывод
    # -------------------------

    output_factories = {
        OutputFormat.CONSOLE: ConsoleOutput,
        OutputFormat.JSON: JsonOutput,
        OutputFormat.CSV: CsvOutput,
    }

    output_factory = OutputFactory(output_factories)
    output_handler = output_factory.create(output, report)

    output_handler.output()


if __name__ == "__main__":
    app()