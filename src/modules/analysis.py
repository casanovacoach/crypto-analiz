def extract_coin_fields(data):
    coins = []
    for coin in data:
        record = {
            'name': coin['name'],
            'symbol' : coin['symbol'],
            'change24percentage': coin['price_change_percentage_24h'] or 0,
            'volume': coin['total_volume'] or 0,
            'market_cap': coin['market_cap'] or 0
        }
        coins.append(record)
    return coins


# Сортируем за 24 часа по убыванию
def get_top_gainers(data_coins, n=3):
    up_change = sorted(
        data_coins,
        key=lambda x: x['change24percentage'],
        reverse=True)

    return up_change[:n]


# Сортируем за 24 часа по возрастанию
def get_top_losers(data_coins, n=3):
    down_change = sorted(
        data_coins,
        key=lambda x: x['change24percentage'],
        reverse=False)
    return down_change[:n]


# Самая крупная монета по объёму торгов СОРТ
def get_top_value_coin(data_coins):
    return max(
        data_coins,
        key=lambda x: x['volume'])


# Сумма капитализации 50ти монет.
def get_sum_market_cap(data_coins):
    sum_market_cap = sum(
        coin['market_cap']
        for coin in data_coins)

    return sum_market_cap