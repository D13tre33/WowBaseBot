from uuid import uuid4

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from tgbot.handlers.su.utils import SuRouter
from tgbot.keyboards.menu.admins.admins import admins_keyboard
from tgbot.misc.actions import NavigationAction
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings

add_router = SuRouter()


@add_router.callback_query(NavigationAction.filter(F.to == "add_admin"))
async def su_add_admin_menu(callback_query: CallbackQuery, state: FSMContext):
    deep_link_hash = "aa-" + str(uuid4())

    await Storage.deep_links.add(deep_link_hash)

    deep_link = await create_start_link(
        bot=state.bot,
        payload=deep_link_hash,
        encode=True
    )

    await callback_query.message.edit_text(
        text=strings.admins().successful_addition(deep_link),
        parse_mode="MarkdownV2"
    )
    await callback_query.message.edit_reply_markup(
        reply_markup=admins_keyboard,
    )
