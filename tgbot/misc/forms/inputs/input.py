from aiogram import Bot
from aiogram.types import Message

from tgbot.misc.base import Base
from tgbot.misc.forms.inputs.validators.validator import Validator, validator, \
    username_validator, count_validator, user_id_validator, datatime_validator, uuid4_validator, \
    chat_availability_validator, phone_number_validator, email_validator


class Input(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        name: str = dict_.get("name")
        title: str = dict_.get("title", "")
        label: str = dict_.get("label")
        description: str = dict_.get("description")
        error: str = dict_.get("error")
        validators: list[Validator] = dict_.get("validators", [validator()])
        markdown: bool = dict_.get("markdown", True)

        self.name = name
        self.title = title
        self.label = label
        self.description = description
        self.error = error
        self.validators = validators
        self.markdown = markdown

        dict.__init__(
            self,
            name=name,
            title=title,
            label=label,
            description=description,
            error=error,
            validators=validators,
            markdown=markdown,
        )

    async def validate(self, bot: Bot, message: Message) -> bool:
        for validator_ in self.validators:
            validator_ = validator(**validator_)
            if not await validator_.validate(bot=bot, message=message, markdown=self.markdown):
                return False
        return True


def text_input(**kwargs) -> Input:
    return Input(kwargs)


def email_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [email_validator()]
    })
    return text_input(**kwargs)


def phone_number_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [phone_number_validator()]
    })
    return text_input(**kwargs)


def username_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [username_validator()]
    })
    return text_input(**kwargs)


def chat_id_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [username_validator(), chat_availability_validator()]
    })
    return text_input(**kwargs)


def count_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [count_validator()]
    })
    return text_input(**kwargs)


def user_id_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [user_id_validator()]
    })
    return text_input(**kwargs)


def datatime_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [datatime_validator()]
    })
    return text_input(**kwargs)


def uuid4_input(**kwargs) -> Input:
    kwargs.update({
        "markdown": False,
        "validators": [uuid4_validator()]
    })
    return text_input(**kwargs)
