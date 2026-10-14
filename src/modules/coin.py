class Coin:

    def __init__(self, name, symbol, change_24h, volume, market_cap):
        if name.strip() != '':
            self.name = name.strip()
        else:
            raise ValueError('Coin name cannot be empty')

        if symbol.strip() != '':
            self.symbol = symbol.strip()
        else:
            raise ValueError('Coin symbol cannot be empty')

        self.change_24h = change_24h
        if volume >= 0:
            self.volume = volume
        else:
            raise ValueError('Coin volume cannot be negative')

        if market_cap >= 0:
            self.market_cap = market_cap
        else:
            raise ValueError('Coin market cap cannot be negative')


    def __lt__(self, other: Coin):
        if not isinstance(other, Coin):
            return NotImplemented
        return self.change_24h < other.change_24h


    def __gt__(self, other: Coin):
        if not isinstance(other, Coin):
            return NotImplemented
        return self.change_24h > other.change_24h


    def __repr__(self):
        return f'{self.name} {self.symbol} {self.change_24h:+.2f}'


    def __str__(self):
        return f'{self.name} {self.symbol} изменение за 24 часа: {self.change_24h:+.2f}%'


class CoinCollection:
    def __init__(self, coins):
        self.coins = coins

    def top_gainers(self, n=3):
        return sorted(self.coins, reverse=True)[:n]

    def top_losers(self, n=3):
        return sorted(self.coins)[:n]

    def top_volume(self):
        return max(self.coins, key=lambda coin: coin.volume)

    def total_market_cap(self):
        return sum(coin.market_cap for coin in self.coins)

    def __iter__(self):
        return iter(self.coins)

    def __len__(self):
        return len(self.coins)