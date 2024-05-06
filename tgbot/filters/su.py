from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config
from tgbot.misc.storage.storage import Storage


class SUFilter(BaseFilter):
    is_su: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return ((obj.from_user.id in config.tg_bot.su_ids) == self.is_su and
                not await Storage.admins.get_common_user_mode(obj.from_user.id))
