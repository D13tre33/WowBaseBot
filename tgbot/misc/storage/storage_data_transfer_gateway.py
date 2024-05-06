from tgbot.misc.storage.storage_common import StorageCommon
from tgbot.models.data_transfer_gateway import DataTransferGateway, data_transfer_gateway


class StorageDataTransferGateway:

    @staticmethod
    async def get(global_data: dict = None) -> DataTransferGateway:
        return data_transfer_gateway(**await StorageCommon.get_data(global_data))

    @staticmethod
    async def save(data_transfer_gateway_: DataTransferGateway, global_data: dict = None):
        global_data = await StorageCommon.get_data(global_data)
        # global_data["data_transfer_gateway"] = data_transfer_gateway_
        global_data.update(data_transfer_gateway_)
        await StorageCommon.save(global_data)
