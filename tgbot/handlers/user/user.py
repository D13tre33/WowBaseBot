from tgbot.handlers.user.deep_links import deep_links_router
from tgbot.handlers.user.main_menu import main_menu_router
from tgbot.handlers.user.utils import UserRouter

user_router = UserRouter()

user_router.include_router(main_menu_router)
user_router.include_router(deep_links_router)
