from aiogram.fsm.state import State

from tgbot.misc.states.states import Navigator
from tgbot.misc.strings import strings


class Screen:
    id: str
    title: str
    state: State

    def __init__(self, screen_id: str, title: str, state: State):
        self.id = screen_id
        self.title = title
        self.state = state  # TODO убрать?


Screens = {
    "main": Screen(
        screen_id="main",
        title=strings.base().main_menu,
        state=Navigator.main
    ),
    "admins": Screen(
        screen_id="admins",
        title=strings.admins().short_title,
        state=Navigator.admins
    ),
    "add_admin": Screen(
        screen_id="add_admin",
        title=strings.admins().add,
        state=Navigator.add_admin
    ),
    "remove_admin": Screen(
        screen_id="remove_admin",
        title=strings.admins().remove,
        state=Navigator.remove_admin
    ),
    "admins_list": Screen(
        screen_id="admins_list",
        title=strings.base().list,
        state=Navigator.admins_list
    ),
}
