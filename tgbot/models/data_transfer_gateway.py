from tgbot.misc.base import Base


class DataTransferGateway(Base):

    def __init__(self, global_data: dict):
        super().__init__()

        data: dict = global_data.get("data_transfer_gateway", {})

        keys: dict = data.get("keys", {})
        storage: dict = data.get("storage", {})

        data.update({
            "keys": keys,
            "storage": storage,
        })

        self.keys = keys
        self.storage = storage

        dict.__init__(self, data_transfer_gateway=data)

    def set_data(self, uuid: str, key, data):
        self.keys[uuid] = key
        self.storage[uuid] = data

    def get_data(self, uuid: str, key):
        if self.keys[uuid] == key:
            data = self.storage[uuid]
            del self.storage[uuid]
            return data
        return None


def data_transfer_gateway(**kwargs) -> DataTransferGateway:
    return DataTransferGateway(kwargs)
