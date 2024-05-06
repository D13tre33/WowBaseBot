from enum import Enum

from aiogram.filters.callback_data import CallbackData


class NavigatorAction(str, Enum):
    navigate = "navigate"
    back = "back"


class NavigationAction(CallbackData, prefix="su"):
    action: NavigatorAction
    to: str


class QuickAction(CallbackData, prefix="qa"):
    level: str
    type: str
