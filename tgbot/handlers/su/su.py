from tgbot.handlers.su.admins.admins import admins_router
from tgbot.handlers.su.main_menu import main_menu_router
from tgbot.handlers.su.utils import SuRouter

su_router = SuRouter()

su_router.include_router(main_menu_router)
su_router.include_router(admins_router)
