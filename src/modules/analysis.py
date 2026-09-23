from abc import ABC, abstractmethod

class Analysis(ABC):

    def __init__(self, data):
        self.data = self.extract_coin_fields(data)

    @abstractmethod
    def analyze(self):
        pass

    @staticmethod
    def extract_coin_fields(data):
        coins = []
        for coin in data:
            record = {
                'name': coin['name'],
                'symbol': coin['symbol'],
                'change24percentage': coin['price_change_percentage_24h'] or 0,
                'volume': coin['total_volume'] or 0,
                'market_cap': coin['market_cap'] or 0
            }
            coins.append(record)
        return coins


class GainersAnalysis(Analysis):

    """Сортирует топ 3 монеты подъёма за 24 часа"""

    def analyze(self):
        up_change = sorted(
            self.data,
            key=lambda x: x['change24percentage'],
            reverse=True)

        return up_change[:3]

class LosersAnalysis(Analysis):

    """Сортирует топ 3 монеты падения за 24 часа"""

    def analyze(self):
        down_change = sorted(
            self.data,
            key=lambda x: x['change24percentage'],
            reverse=False)
        return down_change[:3]


class TopValueAnalysis(Analysis):

    """Самая крупная монета по объёму торгов"""

    def analyze(self):
        return max(
            self.data,
            key=lambda x: x['volume'])


class MarketCapAnalysis(Analysis):

    """Сумма капитализации 50ти монет."""

    def analyze(self):

        return sum(coin['market_cap'] for coin in self.data)