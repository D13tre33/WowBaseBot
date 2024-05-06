from tgbot.handlers.admin.actions import actions_router
from tgbot.handlers.admin.main_menu import main_menu_router
from tgbot.handlers.admin.misc import misc_router
from tgbot.handlers.admin.utils import AdminRouter

admin_router = AdminRouter()

admin_router.include_router(actions_router)
admin_router.include_router(main_menu_router)
admin_router.include_router(misc_router)
