import json
from typing import Optional

from tgbot.misc.storage.storage_common import StorageCommon
from tgbot.models.user import User, user


class StorageUsers:

    @staticmethod
    async def all(global_data: Optional[dict] = None) -> dict:
        global_data = await StorageCommon.get_data(global_data)
        if "users" not in global_data:
            global_data["users"] = {}
        return global_data["users"]

    @staticmethod
    async def add(user_model: User, global_data: Optional[dict] = None):
        global_data = await StorageCommon.get_data(global_data)
        users = await StorageUsers.all(global_data)
        users[str(user_model.id)] = user_model
        global_data["users"] = users
        await StorageCommon.save(global_data)

    @staticmethod
    async def get(user_id, global_data: Optional[dict] = None) -> User:
        global_data = await StorageCommon.get_data(global_data)
        users_data = await StorageUsers.all(global_data)
        user_id = str(user_id)
        if user_id in users_data:
            user_data = users_data[user_id]
            if type(user_data) is str:
                return user(**json.loads(users_data[user_id]))
            else:
                return user(**users_data[user_id])
        return user(
            id=int(user_id),
            username="None",
            first_name="None",
            last_name="None",
        )
