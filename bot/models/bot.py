class BotResponse:
    def __init__(self, content, reply_markup=None, next_state="", errors=""):
        self.content = content
        self.reply_markup = reply_markup
        self.errors = errors
