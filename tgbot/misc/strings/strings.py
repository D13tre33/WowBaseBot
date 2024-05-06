from tgbot.misc.singleton import Singleton
from tgbot.misc.strings.actions import Actions
from tgbot.misc.strings.base import Base
from tgbot.misc.strings.debug import Debug
from tgbot.misc.strings.menu.admins_menu import AdminsMenu
from tgbot.misc.strings.menu.su_main_menu import SUMainMenu
from tgbot.misc.strings.menu.user_main_menu import UserMainMenu


class Strings(Singleton):

    @staticmethod
    def base():
        return Base()

    @staticmethod
    def actions():
        return Actions()

    @staticmethod
    def debug():
        return Debug()

    @staticmethod
    def admins():
        return AdminsMenu()

    @staticmethod
    def user_main_menu():
        return UserMainMenu()

    @staticmethod
    def su_main_menu():
        return SUMainMenu()
