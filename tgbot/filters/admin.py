from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config
from tgbot.misc.storage.storage import Storage


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        global_data = await Storage.common.get_data()
        return (await Storage.admins.check_id(obj.from_user.id) and
                not await Storage.admins.get_common_user_mode(obj.from_user.id, global_data))
