from typing import Optional, List

from tgbot.misc.storage.storage_common import StorageCommon
from tgbot.misc.storage.storage_su import StorageSU
from tgbot.misc.storage.storage_users import StorageUsers
from tgbot.models.user import User


class StorageAdmins:

    @staticmethod
    async def get_ext_ids(global_data: Optional[dict] = None) -> List[int]:
        global_data = await StorageCommon.get_data(global_data)
        if "ext_admin_ids" not in global_data:
            global_data["ext_admin_ids"] = []
        return global_data["ext_admin_ids"]

    @staticmethod
    async def set_env_ids(env_admin_ids: List[int]):
        global_data = await StorageCommon.get_data()
        global_data["env_admin_ids"] = env_admin_ids
        await StorageCommon.save(global_data)

    @staticmethod
    async def get_env_ids(global_data: Optional[dict] = None) -> List[int]:
        global_data = await StorageCommon.get_data(global_data)
        if "env_admin_ids" not in global_data:
            global_data["env_admin_ids"] = []
        return global_data["env_admin_ids"]

    @staticmethod
    async def get_ids(global_data: Optional[dict] = None) -> List[int]:
        ids = await StorageAdmins.get_env_ids(global_data) + await StorageAdmins.get_ext_ids(global_data)
        ids += await StorageSU.get_ids(global_data)
        return ids

    @staticmethod
    async def check_id(admin_id: int, global_data: Optional[dict] = None) -> bool:
        ids = await StorageAdmins.get_env_ids(global_data) + await StorageAdmins.get_ext_ids(global_data)
        ids += await StorageSU.get_ids(global_data)
        return admin_id in ids

    @staticmethod
    async def add_id(admin_id) -> bool:
        """
        Returns True if admin_id already exists
        :param admin_id:
        :return: bool
        """
        global_data = await StorageCommon.get_data()
        admin_ids = await StorageAdmins.get_ids(global_data)
        ext_admin_ids = await StorageAdmins.get_ext_ids(global_data)
        if admin_id not in admin_ids:
            ext_admin_ids.append(admin_id)
            ext_admin_ids = list(set(ext_admin_ids))
            global_data["ext_admin_ids"] = ext_admin_ids
            await StorageCommon.save(global_data)
            return False
        return True

    @staticmethod
    async def remove_id(admin_id: int):
        global_data = await StorageCommon.get_data()
        ext_admin_ids = await StorageAdmins.get_ext_ids(global_data)
        if admin_id in ext_admin_ids:
            ext_admin_ids.remove(admin_id)
        global_data["ext_admin_ids"] = ext_admin_ids
        await StorageCommon.save(global_data)

    @staticmethod
    async def get_common_user_mode(user_id: int, global_data: Optional[dict] = None) -> bool:
        user_data = await StorageUsers.get(user_id, global_data)
        if type(user_data) is User:
            return user_data.user_mode_enabled
        return False

    @staticmethod
    async def set_common_user_mode(user_id: int, value: bool, global_data: Optional[dict] = None):
        global_data = await StorageCommon.get_data(global_data)
        user_data = await StorageUsers.get(user_id, global_data)
        if type(user_data) is User:
            user_data.user_mode_enabled = value
            user_data["user_mode_enabled"] = value
            await StorageUsers.add(user_data)
