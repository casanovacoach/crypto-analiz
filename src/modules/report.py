import datetime

class Report:
    def __init__(self,
                 data_coins,
                 top_gainers,
                 top_losers,
                 market_cap,
                 top_value_coin):

        self.generated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.total_coins_analyzed = len(data_coins)
        self.total_market_cap_usd = market_cap

        self.top_gainers = [
            self.coin_to_report(coin)
            for coin in top_gainers
            ]

        self.top_losers = [
            self.coin_to_report(coin)
            for coin in top_losers
            ]

        self.highest_volume = self.coin_to_highest_volume_report(top_value_coin)


    @staticmethod
    def coin_to_report(coin):
        return {
                "name": coin['name'],
                "symbol": coin['symbol'],
                "change_24h": round(coin['change24percentage'], 1),
                }


    @staticmethod
    def coin_to_highest_volume_report(coin):
        return {
                "name" : coin['name'],
                "symbol": coin["symbol"],
                "volume_usd": coin['volume'],
                }