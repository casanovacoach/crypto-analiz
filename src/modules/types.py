from enum import Enum


class Source(str, Enum):
    COINGECKO = "coingecko"
    COINMARKETCAP = "coinmarketcap"


class OutputFormat(str, Enum):
    CONSOLE = "console"
    JSON = "json"
    CSV = "csv"