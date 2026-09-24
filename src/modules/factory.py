from collections.abc import Callable

from modules.api_request import (
    APIRequest,
    CoinGeckoRequest,
    CoinMarketCapRequest,
)
from modules.types import Source, OutputFormat


class ProviderFactory:
    def __init__(self, providers: dict[Source, Callable[[], APIRequest]]):
        self.providers = providers

    def create(self, source: Source) -> APIRequest:
        return self.providers[source]()


class OutputFactory:
    def __init__(self, outputs):
        self.outputs = outputs

    def create(self, output_format, report):
        return self.outputs[output_format](report)