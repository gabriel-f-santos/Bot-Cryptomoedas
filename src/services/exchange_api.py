from abc import ABC, abstractmethod

class ExchangeAPIABC(ABC):

    @abstractmethod
    def iniciar_conexao(self):
        pass


class ExchangeAPI(ExchangeAPIABC):

    def __init__(self, api_key, secret_key, conexao, test=True) -> None:
        self.api_key = api_key 
        self.secret_key = secret_key
        self.conexao = conexao
        self.test = test

    def iniciar_conexao(self):
        return self.conexao(self.api_key, self.secret_key, test=self.test)
