
from binance import Client

def conexao_binance_api(api_key, secret_key, tld=None, test=True):
    if test:
        client = Client(api_key, secret_key, tld=tld, testnet=test)
    else:
        client = Client(api_key, secret_key)
    return client
