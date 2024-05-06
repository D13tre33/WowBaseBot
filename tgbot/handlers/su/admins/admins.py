from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.handlers.su.admins.add import add_router
from tgbot.handlers.su.admins.remove import remove_router
from tgbot.handlers.su.utils import SuRouter
from tgbot.keyboards.menu.admins.admins import admins_keyboard
from tgbot.misc.actions import NavigationAction
from tgbot.misc.states.states import Navigator
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings
from tgbot.models.user import User

admins_router = SuRouter()
admins_router.include_router(add_router)
admins_router.include_router(remove_router)


@admins_router.callback_query(NavigationAction.filter(F.to == "admins"))
async def su_admins_menu(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Navigator.idle)

    text = strings.admins().title

    if type(callback_query.message) is Message:
        await callback_query.message.edit_text(
            text=text,
            parse_mode="MarkdownV2"
        )
        await callback_query.message.edit_reply_markup(
            reply_markup=admins_keyboard,
        )
    else:
        await state.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=text,
            parse_mode="MarkdownV2",
            reply_markup=admins_keyboard
        )


@admins_router.callback_query(NavigationAction.filter(F.to == "admins_list"))
async def su_admins_list(callback_query: CallbackQuery):
    admins_strings = strings.admins()

    admin_ids = await Storage.admins.get_ids()

    if len(admin_ids) > 0:
        text = f"{admins_strings.list}:\n\n"
        for admin_id in admin_ids:
            admin_id_key = str(admin_id)
            admin_info = await Storage.users.get(admin_id_key)
            if type(admin_info) is User:
                text += f"{admins_strings.admin_info(admin_info)}\n"
            else:
                text += f"{admins_strings.admin_info_none(admin_id)}\n\n"
        await callback_query.message.edit_text(
            text=text,
            parse_mode="MarkdownV2"
        )
        await callback_query.message.edit_reply_markup(
            reply_markup=admins_keyboard,
        )
    else:
        await callback_query.message.edit_text(
            text=admins_strings.empty_list,
            parse_mode="MarkdownV2"
        )
        await callback_query.message.edit_reply_markup(
            reply_markup=admins_keyboard,
        )
