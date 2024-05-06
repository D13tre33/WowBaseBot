from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.handlers.su.utils import SuRouter
from tgbot.keyboards.menu.admins.admins import admins_keyboard
from tgbot.misc.forms.form import FormResultData, form
from tgbot.misc.states.states import Navigator
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings

remove_router = SuRouter()


@remove_router.callback_query(FormResultData.filter(F.uuid == "remove_admin_form"))
async def su_remove_admin_finish(callback_query: CallbackQuery, state: FSMContext, callback_data: FormResultData):
    await state.set_state(Navigator.idle)
    try:
        data_transfer_gateway_ = await Storage.data_transfer_gateway.get()
        form_ = form(**data_transfer_gateway_.get_data(callback_data.data_transfer_uuid, callback_query.from_user.id))
        admin_id = int(form_.data["user_id"])
        admin_ids = await Storage.admins.get_ids()
        if len(admin_ids) > 0:
            if admin_id in admin_ids:
                await Storage.admins.remove_id(admin_id)
                text = strings.admins().successful_removing(admin_id)
            else:
                text = strings.admins().admin_not_founded(admin_id)
        else:
            text = strings.admins().empty_list_message
    except BaseException:
        text = strings.base().something_went_wrong

    await state.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=admins_keyboard
    )
