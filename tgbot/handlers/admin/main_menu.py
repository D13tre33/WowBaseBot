from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from tgbot.handlers.admin.utils import AdminRouter
from tgbot.keyboards.menu.main import admin_main_keyboard
from tgbot.misc.actions import NavigationAction
from tgbot.misc.states.states import Navigator
from tgbot.misc.strings import strings

main_menu_router = AdminRouter()


@main_menu_router.message(Command("menu"))
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(Navigator.idle)

    menu = await get_hello_menu()

    await message.answer(
        text=menu[0],
        reply_markup=menu[1],
        parse_mode="MarkdownV2"
    )


@main_menu_router.callback_query(NavigationAction.filter(F.to == "main"))
async def admin_main_menu(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Navigator.idle)

    menu = await get_hello_menu()

    await callback_query.message.edit_text(
        text=menu[0],
        parse_mode="MarkdownV2"
    )

    await callback_query.message.edit_reply_markup(
        reply_markup=menu[1]
    )


async def get_hello_menu() -> tuple[str, InlineKeyboardMarkup]:
    text = strings.admins().hello
    keyboard = admin_main_keyboard

    return text, keyboard
