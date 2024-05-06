from aiogram.types import InlineKeyboardButton

from tgbot.misc.actions import NavigationAction, NavigatorAction
from tgbot.misc.forms.form import FormData
from tgbot.navigator.screens import Screens, Screen


def build_back_button(text: str = "Назад", screen: Screen = Screens["main"]) -> InlineKeyboardButton:
    return build_navigation_button(
        text=text,
        screen=screen,
        action=NavigatorAction.back,
    )


def build_navigation_button(
        screen: Screen,
        text: str = None,
        action: NavigatorAction = NavigatorAction.navigate
) -> InlineKeyboardButton:
    if text is None:
        text = screen.title
    return build_callback_button(
        text=text,
        callback_data=NavigationAction(action=action, to=screen.id).pack()
    )


def build_callback_button(
        text: str,
        callback_data: str
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=callback_data
    )


def send_message_action(
        text: str = "Написать сообщение",
) -> InlineKeyboardButton:
    return build_callback_button(
        text=text,
        callback_data=FormData(
            name="start",
            id="sm",
        ).pack()
    )
