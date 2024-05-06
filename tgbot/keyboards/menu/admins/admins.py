from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.menu.buttons import build_navigation_button, build_back_button, build_callback_button
from tgbot.misc.forms.form import FormData
from tgbot.navigator.screens import Screens

admins_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            build_navigation_button(
                screen=Screens["add_admin"],
            ),
            # build_navigation_button(
            #     screen=Screens["remove_admin"],
            # ),
            build_callback_button(
                text=Screens["remove_admin"].title,
                callback_data=FormData(name="start", id="remove_admin_form", payload=str(None)).pack()
            )
        ],
        [
            build_navigation_button(
                screen=Screens["admins_list"],
            )
        ],
        [
            build_back_button()
        ]
    ]
)

remove_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            build_back_button(
                screen=Screens["admins"]
            ),
        ]
    ]
)
#
# remove_admin_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             build_callback_button(
#                 text=Screens["remove_admin"].title,
#                 callback_data=FormData(id="remove_admin_form").pack()
#             )
#         ]
#     ]
# )
