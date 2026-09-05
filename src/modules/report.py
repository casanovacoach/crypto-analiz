import json
import datetime

from analysis import get_sum_market_cap, get_top_gainers, get_top_losers, get_top_value_coin

def report_generator(data_coins):
    top_gainers = get_top_gainers(data_coins)
    top_losers = get_top_losers(data_coins)


    report = {
        'generated_at': datetime.datetime.now().isoformat(),
        'total_coins_analyzed' : len(data_coins),
        'total_market_cap_usd' : get_sum_market_cap(data_coins),

        'top_gainers' : [
            { "name": coin['name'],
            "symbol": coin['symbol'],
            "change_24h": round(coin['change24percentage'], 1),
            }
            for coin in top_gainers
        ],

        'top_losers' : [
            { "name": coin['name'],
              "symbol": coin['symbol'],
              "change_24h": round(coin['change24percentage'], 1),
                }
                for coin in top_losers
        ],

        'highest_volume' : get_top_value_coin(data_coins)
    }

    with open('crypto_report.json', 'w', encoding='UTF8') as f:
        f.write(json.dumps(report, indent=4, ensure_ascii=False))