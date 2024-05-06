from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from tgbot.misc.storage.storage_admins import StorageAdmins
from tgbot.misc.storage.storage_common import StorageCommon
from tgbot.misc.storage.storage_data_transfer_gateway import StorageDataTransferGateway
from tgbot.misc.storage.storage_deep_links import StorageDeepLinks
from tgbot.misc.storage.storage_forms import StorageForms
from tgbot.misc.storage.storage_mapper import StorageMapper
from tgbot.misc.storage.storage_scheduler import StorageScheduler
from tgbot.misc.storage.storage_su import StorageSU
from tgbot.misc.storage.storage_users import StorageUsers


class Storage:

    common = StorageCommon

    users = StorageUsers
    deep_links = StorageDeepLinks
    admins = StorageAdmins
    su = StorageSU
    forms = StorageForms
    data_transfer_gateway = StorageDataTransferGateway
    mapper = StorageMapper
    scheduler = StorageScheduler

    @staticmethod
    def init(new_state: FSMContext, bot: Bot):
        Storage.common.bot = bot
        Storage.common.state = new_state
        Storage.common.key = StorageKey(
            bot_id=bot.id,
            chat_id=0,
            user_id=0
        )
