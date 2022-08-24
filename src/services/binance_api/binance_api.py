
from binance import Client

def conexao_binance_api(api_key, secret_key, tld=None, test=True):
    client = Client(api_key, secret_key, tld=tld, testnet=test)
    return client