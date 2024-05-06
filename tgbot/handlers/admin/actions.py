from typing import List

from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.handlers.admin.utils import AdminRouter
from tgbot.misc.forms.form import FormResultData, form
from tgbot.misc.states.states import Navigator
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings
from tgbot.models.actions import send_message_action
from tgbot.models.user import user, User

actions_router = AdminRouter()


@actions_router.callback_query(FormResultData.filter(F.uuid == "sm"))
async def send_message_form_finish(callback_query: CallbackQuery, state: FSMContext, callback_data: FormResultData):
    try:
        data_transfer_gateway_ = await Storage.data_transfer_gateway.get()
        form_ = form(**data_transfer_gateway_.get_data(callback_data.data_transfer_uuid, callback_query.from_user.id))

        send_message_action_ = send_message_action(**form_.data)

        try:
            chat_id = None

            if send_message_action_.username_or_id.startswith("@"):
                users_data_ = await Storage.users.all()
                users_data: List[dict] = list(users_data_.values())
                for user_data in users_data:
                    try:
                        user_ = user(**user_data)
                        if type(user_) is User and type(user_.username) is str and len(user_.username) > 0:
                            username = user_.username
                            if not username.startswith("@"):
                                username = f"@{username}"
                            if username == send_message_action_.username_or_id:
                                chat_id = int(user_.id)
                                break
                    finally:
                        continue
                if chat_id is None:
                    chat_id = str(send_message_action_.username_or_id)
            else:
                chat_id = int(send_message_action_.username_or_id)

            await state.bot.send_message(
                chat_id=chat_id,
                text=send_message_action_.text,
                parse_mode="MarkdownV2"
            )
            await state.set_state(Navigator.idle)
            await state.bot.send_message(
                chat_id=callback_query.from_user.id,
                text=strings.actions().message_sent_success(send_message_action_),
                parse_mode="MarkdownV2"
            )
        except TelegramBadRequest as error:
            if error.message.__contains__("chat not found"):
                text = strings.actions().message_sent_chat_not_found_error(send_message_action_)
            else:
                print(error)
                text = strings.base().something_went_wrong
            await state.bot.send_message(
                chat_id=callback_query.from_user.id,
                text=text,
                parse_mode="MarkdownV2",
            )
        except BaseException:
            await state.bot.send_message(
                chat_id=callback_query.from_user.id,
                text=strings.base().something_went_wrong,
                parse_mode="MarkdownV2",
            )
    except BaseException:
        await state.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=strings.base().something_went_wrong,
            parse_mode="MarkdownV2",
        )



