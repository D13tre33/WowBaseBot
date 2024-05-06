from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey


class StorageCommon:

    bot: Bot
    state: FSMContext
    key: StorageKey

    data: Optional[dict] = None

    @staticmethod
    async def get_data(data: Optional[dict] = None) -> dict:
        # if Storage.data is None:
        #     Storage.data = await Storage.state.storage.get_data(
        #         bot=Storage.bot,
        #         key=Storage.key
        #     )
        # return Storage.data
        if data is None:
            return await StorageCommon.state.storage.get_data(
                bot=StorageCommon.bot,
                key=StorageCommon.key
            )
        else:
            return data

    @staticmethod
    async def save(global_data: Optional[dict]):
        # diff = {k: Storage.data[k] for k in set(Storage.data) - set(Storage.last_data)}
        # print(diff)
        # Storage.last_data = Storage.data.copy()
        # new_data = Storage.data
        await StorageCommon.state.storage.set_data(
            bot=StorageCommon.bot,
            key=StorageCommon.key,
            data=global_data
        )
