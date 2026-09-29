from enum import Enum

class Source(Enum):
        COINMARKETCAP = 'coinmarketcap'
        COINGECKO = 'coingecko'

class OutputFormat(Enum):
    CONSOLE = 'console'
    JSON = 'json'
    CSV = 'csv'