

class Sinal:
    """
    Recebe df com valor Close sendo preço de fechamento
    """

    def __init__(self, df):
        self.df = df

    def criar_medias(self):
        df = self.df
        df['media_rapida'] = df.Close.rolling(7).mean()
        df['media_lenta'] = df.Close.rolling(25).mean()

    def confirmar_cruzamento(self):
        ## IF The Fast WAS Above the Slow (to prevent repeat buy signals or delayed)
        delay = 3
        df = self.df
        for i in range(delay):
            faixa = delay - i
            media_rapida = df.media_rapida.iloc[-faixa]
            media_lenta = df.media_lenta.iloc[-faixa]
            if media_lenta > media_rapida:
                return True
        return False

    def sinal_compra(self, media_rapida, media_lenta):
        if self.confirmar_cruzamento() and media_rapida > media_lenta:
            return True
        else:
            return False

    def sinal_venda(self, media_rapida, media_lenta):
        if media_lenta > media_rapida:
            return True
        else:
            return False

    def get_sinal(self, posicao):
        df = self.df
        self.criar_medias()
        media_rapida = df.media_rapida.iloc[-1]
        media_lenta = df.media_lenta.iloc[-1]
        print(f"Média Lenta: {media_lenta} Média Rápida: {media_rapida} posição: {posicao}")
        if posicao == 0:
            return self.sinal_compra(media_rapida, media_lenta)
        elif posicao == 1:
            return self.sinal_venda(media_rapida,media_lenta)
        

