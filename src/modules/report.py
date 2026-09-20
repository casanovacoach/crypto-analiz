import json
import datetime

def report_generator(data_coins, top_gainers, top_losers, market_cap, top_value_coin):

    def coin_to_report(coin):
        return { "name": coin['name'],
              "symbol": coin['symbol'],
              "change_24h": round(coin['change24percentage'], 1),
                }
    def coin_to_highest_volume_report(coin):
        return { "name" : coin['name'],
                 "symbol": coin["symbol"],
                 "volume_usd": coin['volume'],
                 }

    report = {
        'generated_at': datetime.datetime.now().isoformat(),
        'total_coins_analyzed' : len(data_coins),
        'total_market_cap_usd' : market_cap,

        'top_gainers' : [
            coin_to_report(coin)
            for coin in top_gainers
        ],

        'top_losers' : [
            coin_to_report(coin)
            for coin in top_losers
        ],

        'highest_volume' : coin_to_highest_volume_report(
                top_value_coin)
    }

    with open('crypto_report.json', 'w', encoding='UTF8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)