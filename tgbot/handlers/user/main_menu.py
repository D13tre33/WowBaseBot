from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.handlers.user.utils import UserRouter
from tgbot.keyboards.menu.main import user_main_keyboard
from tgbot.misc.actions import NavigationAction
from tgbot.misc.states.states import Navigator
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings

main_menu_router = UserRouter()


@main_menu_router.message(Command("menu"))
async def user_menu(message: Message, state: FSMContext):
    await state.set_state(Navigator.idle)

    user_strings = strings.user_main_menu()

    text = f"{user_strings.hello}"

    text += f"\n\n{user_strings.info}"

    is_admin = await Storage.admins.check_id(message.from_user.id)

    await message.answer(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=user_main_keyboard(is_admin)
    )


@main_menu_router.callback_query(NavigationAction.filter(F.to == "main"))
async def user_menu_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Navigator.idle)

    user_strings = strings.user_main_menu()

    text = f"{user_strings.hello}"

    text += f"\n\n{user_strings.info}"

    is_admin = await Storage.admins.check_id(callback_query.from_user.id)

    await callback_query.message.edit_text(
        text=text,
        parse_mode="MarkdownV2"
    )
    await callback_query.message.edit_reply_markup(
        reply_markup=user_main_keyboard(is_admin)
    )
