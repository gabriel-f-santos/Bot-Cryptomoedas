import telegram

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.bot = self.start_bot()

    def start_bot(self):
        return telegram.Bot(self.token)

    def enviar_mensagem(self, msg):
        chat_id = self.chat_id
        self.bot.sendMessage(chat_id, msg)
