import requests
import time
import functools

API_URL= 'https://api.coingecko.com/api/v3/coins/markets'

API_PARAMS = {'vs_currency' :'usd',
            'order' : 'market_cap_desc',
            'per_page' : 50,
            'page' : 1}

# декоратор для request запросов, возврат ошибок в случае наличия
def retry(max_attempts, delay):
     def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f'Попытка {attempt} не удалась, ждём {delay} секунды, и делаем ещё попытку.')
                        time.sleep(delay)
            raise last_exception

        return wrapper

     return deco

class APIRequest:

    def __init__(self, api_url, params):
        self.api_url = api_url
        self.params = params

    #запрос get к API_URL и возвращаем .json
    @retry(max_attempts=3, delay=2)
    def fetch_coins_data(self):
        response = requests.get(self.api_url, params=self.params, timeout=10)
        response.raise_for_status()
        return response.json()