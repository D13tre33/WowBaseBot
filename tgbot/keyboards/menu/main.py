from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.menu.buttons import build_navigation_button, send_message_action, build_callback_button
from tgbot.misc.forms.form import FormData
from tgbot.misc.strings import strings
from tgbot.navigator.screens import Screens
from tgbot.misc.actions import QuickAction

admin_main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            send_message_action(text=strings.actions().send_message)
        ],
        [
            build_callback_button(
                text="Меню пользователя",
                callback_data=QuickAction(
                    level="base",
                    type="enable_common_user_mode",
                ).pack()
            )
        ],
    ]
)

su_main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            build_navigation_button(
                screen=Screens["admins"],
            ),
        ],
        [
            send_message_action(text=strings.actions().send_message)
        ],
        [
            build_callback_button(
                text="Меню пользователя",
                callback_data=QuickAction(
                    level="base",
                    type="enable_common_user_mode",
                ).pack()
            )
        ],
    ]
)


def user_main_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            build_navigation_button(
                text="Обновить",
                screen=Screens["main"],
            )
        ],
        [
            build_callback_button(
                text="Поддержка",
                callback_data=FormData(
                    name="start",
                    id="support",
                ).pack()
            )
        ]
    ]

    if is_admin:
        inline_keyboard.append([
            build_callback_button(
                text="Админка",
                callback_data=QuickAction(
                    level="base",
                    type="disable_common_user_mode",
                ).pack()
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
