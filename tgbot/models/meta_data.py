from tgbot.misc.base import Base


class MessageMetaData(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        message_id: int = int(dict_.get("message_id"))
        from_chat_id: str = str(dict_.get("from_chat_id"))

        self.message_id = message_id
        self.from_chat_id = from_chat_id

        dict.__init__(
            self,
            message_id=message_id,
            from_chat_id=from_chat_id,
        )


def message_meta_data(**kwargs) -> MessageMetaData:
    return MessageMetaData(kwargs)
