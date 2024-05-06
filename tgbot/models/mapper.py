from typing import Union, Optional

from tgbot.misc.base import Base


class Mapper(Base):

    def __init__(self, global_data: dict):
        super().__init__()

        mapper_: dict = global_data.get("mapper", {})

        self.mapper = mapper_

        dict.__init__(self, mapper=mapper_)

    def get_link(self, key: str, name: str, default: Optional[str] = None) -> Union[str, None]:
        return self.mapper.get(key, {}).get(name, default)

    def set_link(self, key: str, name: str, data: str):
        storage = self.mapper.get(key, {})
        storage[name] = data
        self.mapper[key] = storage

    def del_link(self, key) -> Union[str, None]:
        storage = self.mapper.get(key, {})
        link: Union[str, None] = storage.get(key, None)
        del storage[key]
        self.mapper[key] = storage
        return link


def mapper(**kwargs) -> Mapper:
    return Mapper(kwargs)
