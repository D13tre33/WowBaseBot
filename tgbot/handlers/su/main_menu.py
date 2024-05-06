from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from tgbot.handlers.su.utils import SuRouter
from tgbot.keyboards.menu.main import su_main_keyboard
from tgbot.misc.actions import NavigationAction
from tgbot.misc.strings import strings

main_menu_router = SuRouter()


@main_menu_router.message(Command("menu"))
async def su_menu(message: Message):
    (text, keyboard) = await get_hello_menu()

    await message.answer(
        text=text,
        reply_markup=keyboard,
        parse_mode="MarkdownV2"
    )


@main_menu_router.callback_query(NavigationAction.filter(F.to == "main"))
async def su_main_menu(callback_query: CallbackQuery, state: FSMContext):
    (text, keyboard) = await get_hello_menu()

    if type(callback_query.message) is Message:
        await callback_query.message.edit_text(
            text=text,
            parse_mode="MarkdownV2"
        )
        await callback_query.message.edit_reply_markup(
            reply_markup=keyboard,
        )
    else:
        await state.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=text,
            parse_mode="MarkdownV2",
            reply_markup=keyboard
        )


async def get_hello_menu() -> tuple[str, InlineKeyboardMarkup]:
    text = strings.su_main_menu().hello
    keyboard = su_main_keyboard

    return text, keyboard
