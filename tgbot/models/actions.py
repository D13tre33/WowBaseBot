from tgbot.misc.base import Base


class SendMessageAction(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        username_or_id: str = dict_.get("username_or_id")
        text: str = dict_.get("text")

        self.username_or_id = username_or_id
        self.text = text

        dict.__init__(
            self,
            username=username_or_id,
            text=text
        )


def send_message_action(**kwargs) -> SendMessageAction:
    return SendMessageAction(kwargs)
