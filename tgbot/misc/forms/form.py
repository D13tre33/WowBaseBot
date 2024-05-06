from enum import Enum
from typing import Optional

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message

from tgbot.misc.base import Base
from tgbot.misc.forms.inputs.input import Input, text_input
from tgbot.models.meta_data import message_meta_data


class InputResult(str, Enum):
    SUCCESS = 0
    ERROR = 1
    NOTHING = 2


class Form(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        uuid: str = dict_.get("uuid")
        # parent_screen: str = dict_.get("parent_screen")
        callback_title: str = dict_.get("callback_title")
        callback_data: str = dict_.get("callback_data")
        label: str = dict_.get("label")
        description: str = dict_.get("description")
        success_message: str = dict_.get("success_message")
        inputs: list[Input] = dict_.get("inputs", [])
        data: dict = dict_.get("data", {})
        error: str = dict_.get("error", "")
        filled: bool = dict_.get("filled", len(inputs) < 1)
        confirmation_required: bool = dict_.get("confirmation_required", len(inputs) > 1)
        starts_as_new_thread: bool = dict_.get("starts_as_new_thread", False)
        data_transfer_uuid: str = dict_.get("data_transfer_uuid", "")
        payload: str = dict_.get("payload", "")

        self.uuid = uuid
        # self.parent_screen = parent_screen
        self.callback_title = callback_title
        self.callback_data = callback_data
        self.label = label
        self.description = description
        self.success_message = success_message
        self.inputs = inputs

        for input_ in inputs:
            input_: Input = text_input(**input_)
            if input_.name not in data:
                data[input_.name] = None

        self.data = data
        self.error = error
        self.filled = filled
        self.confirmation_required = confirmation_required
        self.starts_as_new_thread = starts_as_new_thread
        self.data_transfer_uuid = data_transfer_uuid
        self.payload = payload

        dict.__init__(
            self,
            uuid=uuid,
            # parent_screen=parent_screen,
            callback_title=callback_title,
            callback_data=callback_data,
            label=label,
            description=description,
            success_message=success_message,
            inputs=inputs,
            data=data,
            error=error,
            filled=filled,
            confirmation_required=confirmation_required,
            starts_as_new_thread=starts_as_new_thread,
            data_transfer_uuid=data_transfer_uuid,
            payload=payload,
        )

    async def input(self, bot: Bot, message: Message) -> InputResult:
        meta_data = self.get_meta_data()
        answer_messages: dict = dict(meta_data.get("answer_messages", {}))
        for i, input_ in enumerate(self.inputs):
            input_ = text_input(**input_)
            if self.data[input_.name] is None:
                answer_messages.update({
                    input_.name: message_meta_data(
                        message_id=message.message_id,
                        from_chat_id=message.chat.id
                    )
                })
                if await input_.validate(bot=bot, message=message):
                    if input_.markdown:
                        text = message.md_text
                        # self.data[input_.name] = message.md_text.replace("|", "")
                    else:
                        text = message.text
                        # self.data[input_.name] = message.text.replace("|", "")
                    if type(text) is not str:
                        text = ""
                    self.put_data(input_.name, text.replace("|", ""))
                    # TODO проблема со спойлерами
                    if i >= len(self.inputs) - 1:
                        self.filled = True
                    meta_data["answer_messages"] = answer_messages
                    self.save_meta_data(meta_data)
                    return InputResult.SUCCESS
                else:
                    self.error = input_.error
                    meta_data["answer_messages"] = answer_messages
                    self.save_meta_data(meta_data)
                    return InputResult.ERROR
        meta_data["answer_messages"] = answer_messages
        self.save_meta_data(meta_data)
        return InputResult.NOTHING

    def get_meta_data(self) -> dict:
        return dict(self.data.get("__meta__", {}))

    def save_meta_data(self, meta_data: dict):
        self.put_data("__meta__", meta_data)

    def put_data(self, key: str, value):
        self.data[key] = value

    def next(self) -> Optional[Input]:
        for input_ in self.inputs:
            input_: Input = text_input(**input_)
            if self.data[input_.name] is None:
                return input_
        return None


def form(**kwargs) -> Form:
    return Form(kwargs)


class FormResult(Base):

    def __init__(self, dict_: dict):
        super().__init__()

        uuid: str = dict_.get("uuid")
        data: dict = dict_.get("data")
        error: str = dict_.get("error")
        filled: bool = dict_.get("filled")

        self.uuid = uuid
        self.data = data
        self.error = error
        self.filled = filled

        dict.__init__(
            self,
            uuid=uuid,
            data=data,
            error=error,
            filled=filled,
        )


def form_result(**kwargs) -> FormResult:
    return FormResult(kwargs)


# class BaseData(Base, CallbackData):
#     name: str


class FormData(CallbackData, prefix="form"):
    id: str
    name: str
    payload: str = str(None)


class FormResultData(CallbackData, prefix="form"):
    uuid: str
    data_transfer_uuid: str

    # def __init__(self, **kwargs):
    #     form_: Union[str, Form] = kwargs.get("form")
    #     kwargs.update({
    #         "form": b64encode(str(form_))
    #     })
    #     super().__init__(**kwargs)
    #
    # def _encode_value(self, key: str, value: Any) -> str:
    #     if isinstance(value, Form):
    #         return str(b64encode(str(value)))
    #     return super()._encode_value(key, value)
    #
    # def unpack(self, value: str) -> CallbackData:
    #     result = self.unpack(value)
    #     return result

# class NavigatorAction(str, Enum):
#     navigate = "navigate"
#     back = "back"
#
#
# class NavigationAction(CallbackData, prefix="su"):
#     action: NavigatorAction
#     to: str
