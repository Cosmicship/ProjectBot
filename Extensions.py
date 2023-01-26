import requests
import json
from Confyg import keys

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Невозможно конвертировать одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Ошибка в названии валюты {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Ошибка в названии валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректное количество валюты {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
