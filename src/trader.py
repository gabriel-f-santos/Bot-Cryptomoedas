# encoding: utf-8

from abc import ABC, abstractclassmethod
from datetime import datetime
import math
from data.get_preco_compra.preco_compra import get_preco_compra_db
from data.get_preco_venda.preco_venda import get_preco_venda_db
from data.get_rentabilidade.rentabilidade import get_rentabilidade_db
from data.get_ultima_atualizacao import get_posicao
from data.insert_novo_trade.insert_trade import insert_trade_db
from data.set_preco_compra.set_preco_compra import atualiza_preco_compra_db
from data.set_preco_venda.set_preco_venda import atualiza_preco_venda_db
from data.set_rentabilidade.rentabilidade import atualiza_rentabilidade_db
from data.set_ultima_atualizacao import atualiza_posicao
from services.binance_api.binance_api import conexao_binance_api
from services.exchange_api import ExchangeAPI
from services.telegram_bot.telegram import TelegramBot
from sinal.media_movel import Sinal
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")
token_tg = os.getenv("TOKEN_TELEGRAM")

class TradeCrypto(ABC):

    @abstractclassmethod
    def get_saldo(self, moeda):
        raise NotImplementedError

    @abstractclassmethod
    def get_quantidade_minima_trade(self, moeda):
        raise NotImplementedError

    @abstractclassmethod
    def get_quantidade_trade(self, moeda, valor_fechamento):
        raise NotImplementedError

    @abstractclassmethod
    def get_dados_candle(self, moeda):
        raise NotImplementedError

    @abstractclassmethod
    def executar_trade(self, moeda):
        raise NotImplementedError


class TradeCryptoBynance(TradeCrypto):

    def __init__(self, client):
        self.client = client

    def atualiza_rentabilidade(self, moeda):
        preco_venda = get_preco_venda_db(moeda)
        preco_compra = get_preco_compra_db(moeda)
        rentabilidade = get_rentabilidade_db(moeda)
        print(f"prço venda {preco_venda}")
        print(f"prço compra {preco_compra}")
        try:
            rentabilidade += float(((preco_venda)/(preco_compra))-1)
            print(f"rentabilidade {((preco_venda)/(preco_compra))-1}")
        except:
            pass
        atualiza_rentabilidade_db(moeda, rentabilidade)
        print(f"rentabilidade {rentabilidade}")
        return rentabilidade

    def get_saldo(self, moeda="USDT"):
        saldo = self.client.get_asset_balance(moeda.replace("USDT",""))
        return saldo['free']

    def get_quantidade_minima_trade(self, moeda):
        filtros = self.client.get_symbol_info(f'{moeda}')["filters"]
        quantidade_minima = 0
        for filtro in filtros:
            if filtro["filterType"] == "LOT_SIZE":
                quantidade_minima=filtro['minQty']
        return quantidade_minima

    def get_usdt_holdings(self):
        usdt = self.client.get_asset_balance('USDT')
        print(f"usdt {usdt}")
        return usdt['free']

    def get_quantidade_trade(self, moeda, valor_fechamento, side):
        if side == 'BUY': 
            saldo = float(self.get_usdt_holdings())
            quantidade = float(saldo) / float(valor_fechamento)
        else:
            saldo = float(self.get_saldo(moeda))
            quantidade = float(self.get_saldo(moeda))

        quantidade_minima = int(str(self.get_quantidade_minima_trade(moeda)).count('0')-2)
        quantidade = round(math.floor(quantidade), quantidade_minima)
        # if 'e-' in str(quantidade):
        #     quantidade = 0
        # else:
        #     primeira_posicao = str(quantidade_minima).find('1',)
        #     quantidade_minima = float(str(quantidade_minima)[:primeira_posicao+1])
        #     saldo = float(str(saldo)[:primeira_posicao+1])
        #     quantidade = float(str(quantidade)[:primeira_posicao+1])
        print(f"saldo: {saldo}, qtd: {quantidade}")
        return quantidade

    def get_dados_candle(self, moeda):
        df_candles = pd.DataFrame(self.client.get_historical_klines(moeda,'1h','100 hours ago UTC'))
        df_candles = df_candles.iloc[:,:5]
        df_candles.columns = ['Time','Open','High','Low','Close']
        df_candles[['Open','High','Low','Close']] = df_candles[['Open','High','Low','Close']].astype(float)
        df_candles.Time = pd.to_datetime(df_candles.Time, unit='ms')
        df_candles['Currency'] = moeda
        self.df = df_candles
        return df_candles

    def atualiza_valores_db(self, side, moeda, preco):
        if side == "BUY":
            atualiza_preco_compra_db(moeda, preco)
        else:
            atualiza_preco_venda_db(moeda, preco)

    def executar_trade(self, moeda, posicao):
        log_datetime = datetime.now()
        preco = self.df.Close.iloc[-1]
        if posicao:
            side='BUY'
        else:
            side='SELL'
        quantidade = self.get_quantidade_trade(moeda, preco, side)
        try:
            order = self.client.create_order(symbol=moeda, side=side,type='MARKET',quantity=quantidade)
            _preco = float(order['fills'][0]['price'])
        except Exception as e:
            print(e)
            #write_to_file(f'{moeda}',f'{log_datetime}:Binance Error:{e}')
            erro = 1
        else:
            erro = 0
            insert_trade_db(moeda, quantidade, side, preco)
            self.atualiza_valores_db(side, moeda, preco)
            self.atualiza_rentabilidade(moeda)
        return erro

    def avisar_telegram(self, msg, chat_id=None):
        telegram = TelegramBot(token_tg)
        telegram.enviar_mensagem(msg)

    def iniciar_trade(self, moeda):
        trade = {
            0: "compra",
            1: "venda"
        }
        df = self.get_dados_candle(moeda)
        posicao = get_posicao(moeda)
        sinal = Sinal(df).get_sinal(posicao)
        order = None
        if sinal:
            print(f"Sinal {sinal}")
            order = self.executar_trade(moeda, posicao)
            if order != 1:
                # 0 = compra
                rentabilidade = get_rentabilidade_db(moeda)
                if int(posicao) == 0:
                    msg = f"Moeda {moeda} comprada por {self.df.Close.iloc[-1]} - Rentabilidade {rentabilidade}"
                else:
                    msg = f"Moeda {moeda} vendida por {self.df.Close.iloc[-1]} - Rentabilidade {rentabilidade}"
                posicao = True if int(posicao) == 0 else False
                atualiza_posicao(moeda, posicao)
                self.avisar_telegram(msg)

if __name__ == "__main__":
    exchange = ExchangeAPI(api_key, secret_key, conexao_binance_api, test=True)
    client = exchange.iniciar_conexao()
    App = TradeCryptoBynance(client)
    # App.iniciar_trade("BTCUSDT")
    App.iniciar_trade("ETHUSDT")
