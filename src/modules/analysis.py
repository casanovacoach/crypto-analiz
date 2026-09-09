def extract_coin_fields(data):
    coins = []
    for coin in data:
        record = {
            'name': coin['name'],
            'symbol' : coin['symbol'],
            'change24percentage': coin['price_change_percentage_24h'],
            'volume': coin['total_volume'],
            'market_cap': coin['market_cap']
        }
        coins.append(record)
    return coins


# Сортируем за 24 часа по убыванию
def get_top_gainers(data_coins, n=3):
    up_change = sorted(
        data_coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=True)

    return up_change[:n]


# Сортируем за 24 часа по возрастанию
def get_top_losers(data_coins, n=3):
    down_change = sorted(
        data_coins,
        key=lambda x: x['change24percentage'] or 0,
        reverse=False)
    return down_change[:n]


# Самая крупная монета по объёму торгов СОРТ
def get_top_value_coin(data_coins):
    return max(
        data_coins,
        key=lambda x: x['total_volume'] or 0,
        default=None)


# Сумма капитализации 50ти монет.
def get_sum_market_cap(data_coins):
    sum_market_cap = sum(coin.get('market_cap', 0) for coin in data_coins)
    return sum_market_cap