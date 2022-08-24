import telegram

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot = self.start_bot()

    def start_bot(self):
        return telegram.Bot(self.token)

    def enviar_mensagem(self, msg):
        chat_id = self.bot.get_updates()[-1].message.chat_id
        self.bot.sendMessage(chat_id, msg)
