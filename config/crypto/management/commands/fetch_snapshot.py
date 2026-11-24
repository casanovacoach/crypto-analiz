import requests

from django.core.management.base import BaseCommand
from modules.api_request import CoinGeckoRequest

from decimal import Decimal
from crypto.models import Snapshot, CoinPrice

class Command(BaseCommand):
    help = "Fetch and save cryptocurrency snapshot"

    COINGECKO_URL = 'https://api.coingecko.com/api/v3/coins/markets'

    COINGECKO_PARAMS = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
    }

    def handle(self, *args, **options):
        session = requests.Session()

        provider = CoinGeckoRequest(
            self.COINGECKO_URL,
            self.COINGECKO_PARAMS,
            session,
        )

        with provider:
            coins = provider.fetch_coins_data()

        snapshot = Snapshot.objects.create()

        for coin in coins:
            CoinPrice.objects.create(
                snapshot = snapshot,
                coin_id = coin.coin_id,
                coin_name = coin.name,
                symbol = coin.symbol,
                price = Decimal(str(coin.price)),
            )

        self.stdout.write(f'Получено из API: {len(coins)}')
        self.stdout.write(f'Сохранено в БД: {len(coins)}')