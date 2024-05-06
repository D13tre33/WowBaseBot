from tgbot.misc.storage.storage_common import StorageCommon
from tgbot.models.scheduler import Scheduler, scheduler


class StorageScheduler:

    @staticmethod
    async def get(global_data: dict = None) -> Scheduler:
        return scheduler(**await StorageCommon.get_data(global_data))

    @staticmethod
    async def save(scheduler_: Scheduler, global_data: dict = None):
        global_data = await StorageCommon.get_data(global_data)
        global_data.update(scheduler_)
        await StorageCommon.save(global_data)
