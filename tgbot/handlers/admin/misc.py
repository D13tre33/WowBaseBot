from aiogram import F
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message

from tgbot.handlers.admin.utils import AdminRouter
from tgbot.misc.regex import Regex
from tgbot.misc.states.states import Navigator
from tgbot.misc.strings import strings

misc_router = AdminRouter()


@misc_router.message(invert_f(F.text.startswith("/")), StateFilter(Navigator.idle))
async def admin_free_style_action(message: Message):
    try:
        if Regex.username.match(message.text):
            pass
            # TODO
        else:
            raise Exception("not username")
    except BaseException:
        await message.answer(
            text=strings.base().free_action_interpret_error_message,
            parse_mode="MarkdownV2"
        )
