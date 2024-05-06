from tgbot.misc.storage.storage_common import StorageCommon
from tgbot.models.mapper import Mapper, mapper


class StorageMapper:

    @staticmethod
    async def get(global_data: dict = None) -> Mapper:
        return mapper(**await StorageCommon.get_data(global_data))

    @staticmethod
    async def save(mapper_: Mapper, global_data: dict = None):
        global_data = await StorageCommon.get_data(global_data)
        global_data.update(mapper_)
        await StorageCommon.save(global_data)
