from typing import List, Optional

from tgbot.misc.storage.storage_common import StorageCommon


class StorageSU:

    @staticmethod
    async def set_ids(su_id: List[int], global_data: Optional[dict] = None):
        global_data = await StorageCommon.get_data(global_data)
        global_data["su_id"] = su_id
        await StorageCommon.save(global_data)

    @staticmethod
    async def get_ids(global_data: Optional[dict] = None) -> List[int]:
        global_data = await StorageCommon.get_data(global_data)
        return global_data["su_id"]
