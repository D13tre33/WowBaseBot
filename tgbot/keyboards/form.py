from typing import Optional, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.menu.buttons import build_navigation_button, build_callback_button
from tgbot.misc.forms.form import Form, FormData, FormResultData
from tgbot.misc.strings import strings
from tgbot.navigator.screens import Screens


def form_keyboard(form_: Optional[Form] = None) -> InlineKeyboardMarkup:
    if form_ is not None:
        main_row: List[InlineKeyboardButton] = []
        if type(form_.callback_data) is str and type(form_.callback_title) is str and \
                len(form_.callback_data) > 0 and len(form_.callback_title) > 0:
            # main_callback_button = build_callback_button(
            #     text=form_.callback_title,
            #     callback_data=form_.callback_data
            # )
            main_row.append(build_callback_button(
                text=form_.callback_title,
                callback_data=form_.callback_data
            ))
        if form_.filled:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    # [
                    #     build_navigation_button(
                    #         text=strings.base().to_menu,
                    #         screen=Screens[form_.parent_screen],
                    #     ),
                    # ],
                    main_row,
                    [
                        build_callback_button(
                            text=strings.base().repeat,
                            callback_data=FormData(
                                name="start",
                                id=form_.uuid,
                                payload=form_.payload
                            ).pack()
                        )
                    ],
                    [
                        build_callback_button(
                            text=strings.base().confirm,
                            callback_data=FormResultData(
                                uuid=form_.uuid,
                                data_transfer_uuid=form_.data_transfer_uuid
                            ).pack()
                        )
                    ],
                ]
            )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                # [
                #     build_navigation_button(
                #         text=strings.base().to_menu,
                #         screen=Screens[form_.parent_screen],
                #     ),
                # ],
                main_row,
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                build_navigation_button(
                    screen=Screens["main"],
                ),
            ]
        ]
    )
