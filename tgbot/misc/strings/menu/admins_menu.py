from tgbot.misc.singleton import Singleton
from tgbot.misc.strings.base import Base
from tgbot.misc.strings.escape import escape
from tgbot.models.user import User


class AdminsMenu(Singleton):
    hello = "Hello, Admin\\!"

    title = "Управление админами"
    short_title = "Админы"
    add = "Пригласить"
    remove = "Удалить"

    list = "Список админов"
    empty_list_message = "Список админов пуст \\.\\.\\."

    remove_admin_start_message = "Отправь *ID* админа, которого хочешь исключить \\.\\.\\."

    successful_addition_message = "Одноразовая пригласительная ссылка для нового админа"

    bad_admin_id_message_format = "Неверный формат *ID* админа \\.\\.\\."

    welcome_admin_action_message = "Вы перешли по пригласительной ссылке для новых админов\\!"
    welcome_admin_success_message = "Поздравляем, Вы стали админом\\!"
    welcome_admin_exists_message = "Вы уже админ, поэтому ничего не изменилось :\\)"

    @staticmethod
    def successful_addition(deep_link: str):
        return f"{AdminsMenu.successful_addition_message}:\n`{escape(deep_link)}`"

    @staticmethod
    def successful_removing(admin_id: int):
        return f"Админ *`{admin_id}`* удалён из списка админов \\.\\.\\."

    @staticmethod
    def admin_not_founded(admin_id: int):
        return f"Админ *`{admin_id}`* не найден в списке админов \\.\\.\\."

    @staticmethod
    def admin_info(admin_info: User):
        base_strings = Base
        return f"*{admin_info.id}*\n" \
               f"||{base_strings.first_name} \\- *{escape(admin_info.first_name)}*\n" \
               f"{base_strings.last_name} \\- *{escape(admin_info.last_name)}*\n" \
               f"{base_strings.user_name} \\- *@{escape(admin_info.username)}*\n" \
               f"{base_strings.location} \\- *{escape(str(admin_info.location))}*\n||"

    @staticmethod
    def admin_info_none(admin_id: str):
        return f"*{admin_id}* \\- *None*"
