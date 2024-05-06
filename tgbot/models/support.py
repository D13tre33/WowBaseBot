from tgbot.misc.base import Base


class Support(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        text: str = dict_.get("text")

        self.text = text

        dict.__init__(
            self,
            text=text
        )


def support(**kwargs) -> Support:
    return Support(kwargs)
