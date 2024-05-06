from aiogram import Router

from tgbot.filters.su import SUFilter


class SuRouter(Router):

    def __init__(self):
        super().__init__()
        self.message.filter(SUFilter())
        self.callback_query.filter(SUFilter())
