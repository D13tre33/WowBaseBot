import re
from datetime import datetime

from aiogram import Bot
from aiogram.types import Message

from tgbot.misc.base import Base
from tgbot.misc.regex import Regex
from tgbot.misc.utils import check_user_admin_permissions


class Validator(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        pattern: str = dict_.get("pattern", None)
        check_type: str = dict_.get("check_type", "match")

        self.pattern = pattern
        self.check_type = check_type

        dict.__init__(self, pattern=pattern, check_type=check_type)

    async def validate(self, bot: Bot, message: Message, markdown: bool) -> bool:
        text = message.md_text if markdown else message.text
        match self.check_type:
            case ":datetime:":
                try:
                    entered_datetime = datetime.strptime(text, '%Y/%m/%d %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
                    return type(entered_datetime) is str and len(entered_datetime) > 0
                except BaseException:
                    return False
            case ":chat_availability:":
                try:
                    admin_id = int(message.from_user.id)
                    chat_id = text
                    admin_is_admin = await check_user_admin_permissions(bot, admin_id, chat_id)
                    return admin_is_admin
                except BaseException:
                    return False
            case "findall":
                if type(self.pattern) is str:
                    return bool(re.compile(self.pattern).findall(text))
            case _:
                if type(self.pattern) is str:
                    return bool(re.compile(self.pattern).match(text))
        return len(text) > 0

#
# class DateTimeValidator(Validator):
#
#     async def validate(self, bot: Bot, message: Message) -> bool:
#         try:
#             entered_datetime = datetime.strptime(message.text, '%Y/%m/%d %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
#             return type(entered_datetime) is str and len(entered_datetime) > 0
#         except BaseException:
#             return False
#
#
# class ChatAvailabilityValidator(Validator):
#
#     async def validate(self, bot: Bot, message: Message) -> bool:
#         try:
#             admin_id = int(message.from_user.id)
#             channel_id = message.text
#             admin_is_admin = await check_user_admin_permissions(bot, admin_id, channel_id)
#             return admin_is_admin
#         except BaseException:
#             return False


def validator(**kwargs) -> Validator:
    return Validator(kwargs)


def email_validator() -> Validator:
    return validator(pattern=Regex.email.pattern)


def phone_number_validator() -> Validator:
    return validator(pattern=Regex.phone_number.pattern, check_type="findall")


def username_validator() -> Validator:
    return validator(pattern=Regex.username.pattern)


def int_validator() -> Validator:
    return validator(pattern=Regex.int.pattern)


def username_or_id_validator() -> Validator:
    return validator(pattern=Regex.username_or_id.pattern)


def count_validator() -> Validator:
    return validator(pattern=Regex.count.pattern)


def user_id_validator() -> Validator:
    return validator(pattern=Regex.user_id.pattern)


def uuid4_validator() -> Validator:
    return validator(pattern=Regex.uuid4.pattern)


def datatime_validator() -> Validator:
    return validator(check_type=":datetime:")


def chat_availability_validator() -> Validator:
    return validator(check_type=":chat_availability:")
