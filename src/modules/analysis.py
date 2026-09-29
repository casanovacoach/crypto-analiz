from abc import ABC, abstractmethod


class Analysis(ABC):

    def __init__(self, collection):
        self.collection = collection

    @abstractmethod
    def analyze(self, n=3):
        pass


class GainersAnalysis(Analysis):

    def analyze(self, n=3):
        return self.collection.top_gainers(n)

class LosersAnalysis(Analysis):

    def analyze(self, n=3):
        return self.collection.top_losers(n)


class TopValueAnalysis(Analysis):

    def analyze(self, n=3):
        return self.collection.top_volume()


class MarketCapAnalysis(Analysis):

    def analyze(self, n=3):
        return self.collection.total_market_cap()
