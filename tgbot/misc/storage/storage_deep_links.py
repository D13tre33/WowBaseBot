from typing import Optional, Any

from tgbot.misc.storage.storage_common import StorageCommon


class StorageDeepLinks:

    @staticmethod
    async def all(global_data: Optional[dict] = None) -> dict:
        global_data = await StorageCommon.get_data(global_data)
        if "deep_links" not in global_data:
            global_data["deep_links"] = {}
        return global_data["deep_links"]

    @staticmethod
    async def check_existence(deep_link: str) -> Any:
        deep_links = await StorageDeepLinks.all()
        return deep_link in deep_links and deep_links[deep_link]

    @staticmethod
    async def remove(deep_link_hash: str):
        global_data = await StorageCommon.get_data()
        deep_links = await StorageDeepLinks.all(global_data)
        deep_links.pop(deep_link_hash)
        global_data["deep_links"] = deep_links
        await StorageCommon.save(global_data)

    @staticmethod
    async def add(deep_link_hash: str, deep_link_data: Any = True):
        global_data = await StorageCommon.get_data()
        deep_links = await StorageDeepLinks.all(global_data)
        deep_links[deep_link_hash] = deep_link_data
        global_data["deep_links"] = deep_links
        await StorageCommon.save(global_data)

    @staticmethod
    async def get(deep_link_hash: str) -> Any:
        global_data = await StorageCommon.get_data()
        deep_links = await StorageDeepLinks.all(global_data)
        if deep_link_hash in deep_links:
            return deep_links[deep_link_hash]
        return None
