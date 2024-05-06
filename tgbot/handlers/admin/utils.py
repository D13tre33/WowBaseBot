from aiogram import Router

from tgbot.filters.admin import AdminFilter


class AdminRouter(Router):

    def __init__(self):
        super().__init__()
        self.message.filter(AdminFilter())
        self.callback_query.filter(AdminFilter())
