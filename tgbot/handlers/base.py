from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.config import Config
from tgbot.handlers.admin.main_menu import admin_main_menu
from tgbot.handlers.form import form_router
from tgbot.handlers.su.main_menu import su_main_menu
from tgbot.handlers.user.main_menu import user_menu_callback_query
from tgbot.misc.actions import QuickAction
from tgbot.misc.forms.form import FormResultData, form
from tgbot.misc.states.states import Navigator
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings
from tgbot.misc.strings.escape import escape
from tgbot.models.meta_data import message_meta_data
from tgbot.models.support import support
from tgbot.models.user import user

base_router = Router()

base_router.include_router(form_router)


@base_router.callback_query(FormResultData.filter(F.uuid == "support"))
async def support_form_finish(callback_query: CallbackQuery, state: FSMContext, callback_data: FormResultData,
                              config: Config):
    await state.set_state(Navigator.idle)

    try:
        data_transfer_gateway_ = await Storage.data_transfer_gateway.get()
        form_ = form(**data_transfer_gateway_.get_data(callback_data.data_transfer_uuid, callback_query.from_user.id))

        support_ = support(**form_.data)

        user_ = user(**await Storage.users.get(callback_query.from_user.id))

        admin_ids = await Storage.admins.get_ids()

        text = strings.actions().support_message(support_, user_)

        try:
            form_meta_data = form_.get_meta_data()
            support_ask_message = message_meta_data(**form_meta_data.get("answer_messages", {}).get("text", {}))

            for su_id in config.tg_bot.su_ids:
                await state.bot.forward_message(
                    chat_id=su_id,
                    message_id=support_ask_message.message_id,
                    from_chat_id=support_ask_message.from_chat_id
                )
                await state.bot.send_message(
                    chat_id=su_id,
                    text=strings.actions().support_message_sender_info(user_),
                    parse_mode="MarkdownV2"
                )

            for admin_id in admin_ids:
                try:
                    if int(admin_id) not in map(int, config.tg_bot.su_ids):
                        await state.bot.forward_message(
                            chat_id=admin_id,
                            message_id=support_ask_message.message_id,
                            from_chat_id=support_ask_message.from_chat_id
                        )
                        await state.bot.send_message(
                            chat_id=admin_id,
                            text=strings.actions().support_message_sender_info(user_),
                            parse_mode="MarkdownV2"
                        )
                except BaseException:
                    continue
        except BaseException:
            for su_id in config.tg_bot.su_ids:
                await state.bot.send_message(
                    chat_id=su_id,
                    text=text,
                    parse_mode="MarkdownV2"
                )
                for admin_id in admin_ids:
                    try:
                        if int(admin_id) != int(su_id):
                            await state.bot.send_message(
                                chat_id=admin_id,
                                text=text,
                                parse_mode="MarkdownV2"
                            )
                    except BaseException:
                        continue

        await state.bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Спасибо за обращение\\!",
            parse_mode="MarkdownV2"
        )
    except BaseException:
        for su_id in config.tg_bot.su_ids:
            await state.bot.send_message(
                chat_id=su_id,
                text=f"Ошибка при отправке сообщения в поддержку:"
                     f"\n\n`{str(callback_data.pack())}`"
                     f"\n\n`{str(callback_query.from_user.id)}`"
                     f"\n\n@{escape(str(callback_query.from_user.username))}",
                parse_mode="MarkdownV2",
            )


@base_router.callback_query(QuickAction.filter(F.level == "base"))  # TODO наверное надо его переместить
async def base_quick_action(callback_query: CallbackQuery, state: FSMContext, callback_data: QuickAction, config: Config):
    match callback_data.type:
        case "enable_common_user_mode":
            await Storage.admins.set_common_user_mode(callback_query.from_user.id, True)
            await user_menu_callback_query(callback_query, state)
        case "disable_common_user_mode":
            await Storage.admins.set_common_user_mode(callback_query.from_user.id, False)
            if callback_query.from_user.id in config.tg_bot.su_ids:
                await su_main_menu(callback_query, state)
            elif await Storage.admins.check_id(callback_query.from_user.id):
                await admin_main_menu(callback_query, state)
            else:
                await user_menu_callback_query(callback_query, state)
