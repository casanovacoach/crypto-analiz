from abc import ABC, abstractmethod

class Analysis(ABC):

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def analyze(self):
        pass

class GainersAnalysis(Analysis):

    """Сортирует топ 3 монеты подъёма за 24 часа"""

    def analyze(self, top):
        up_change = sorted(
            self.data,
            key=lambda x: x['change24percentage'],
            reverse=True)

        return up_change[:top]

class LosersAnalysis(Analysis):

    """Сортирует топ 3 монеты падения за 24 часа"""

    def analyze(self, top):
        down_change = sorted(
            self.data,
            key=lambda x: x['change24percentage'],
            reverse=False)
        return down_change[:top]


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