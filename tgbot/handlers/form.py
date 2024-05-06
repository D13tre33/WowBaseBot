from uuid import uuid4

from aiogram import Router, F, Dispatcher, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, Update

from tgbot.keyboards.form import form_keyboard
from tgbot.misc.forms.form import form, InputResult, FormData, FormResultData
from tgbot.misc.forms.inputs.input import text_input
from tgbot.misc.states.states import Form
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings

form_router = Router()


@form_router.callback_query(FormData.filter(F.name == "start"))
async def form_start(callback_query: CallbackQuery, state: FSMContext, callback_data: FormData):
    try:
        form_ = form(**await Storage.forms.get(callback_data.id))
        form_.payload = callback_data.payload
        form_["payload"] = callback_data.payload  # TODO ...
        await state.set_data(form_)
        question = form_.next()
        if question is not None:
            await state.set_state(Form.ask)
            text = f"{question.label}\n\n{question.description}"
        else:
            await state.set_state(Form.finish)
            text = "Форма заполнена\\!"
        if not form_.starts_as_new_thread:
            await callback_query.message.edit_text(
                text=text,
                parse_mode="MarkdownV2"
            )
            await callback_query.message.edit_reply_markup(
                reply_markup=form_keyboard(form_)
            )
        else:
            await state.bot.send_message(
                chat_id=callback_query.from_user.id,
                text=text,
                parse_mode="MarkdownV2",
                reply_markup=form_keyboard(form_)
            )
    except BaseException:
        print("@form_router.callback_query `form_start` error")
        text = strings.base().something_went_wrong
        await state.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=text,
            parse_mode="MarkdownV2",
        )


@form_router.message(StateFilter(Form.ask))
async def form_answer(message: Message, state: FSMContext, dispatcher: Dispatcher, bot: Bot, event_update: Update):
    try:
        form_ = form(**await state.get_data())
        input_result: InputResult = await form_.input(bot=bot, message=message)
        match input_result:
            case InputResult.SUCCESS:
                question = form_.next()
                if question is not None:
                    await state.set_state(Form.ask)
                    text = f"{question.label}\n\n{question.description}"
                    await state.set_data(form_)
                else:
                    form_.data_transfer_uuid = str(uuid4())
                    global_data = await Storage.common.get_data()
                    data_transfer_gateway_ = await Storage.data_transfer_gateway.get(global_data)
                    data_transfer_gateway_.set_data(form_.data_transfer_uuid, message.from_user.id, form_)
                    await Storage.data_transfer_gateway.save(data_transfer_gateway_, global_data)
                    if form_.confirmation_required:
                        # await state.set_state(Form.finish)
                        text = f"Форма заполнена\\!\n\n*Проверь, всё ли верно \\.\\.\\.*\n\n"
                        for input_ in form_.inputs:
                            input_ = text_input(**input_)  # TODO why?
                            value = form_.data.get(input_.name)
                            if not input_.markdown:
                                value = f"`{value}`"
                            text += f"*{input_.title}*:\n{value}\n\n"
                    else:
                        await state.set_state(Form.finish)
                        new_event_update = event_update.copy(
                            update={
                                "message": None,
                                "callback_query": CallbackQuery(
                                    id=message.message_id,
                                    from_user=message.from_user,
                                    chat_instance=str(message.chat.id),
                                    data=FormResultData(
                                        uuid=form_.uuid,
                                        data_transfer_uuid=form_.data_transfer_uuid
                                    ).pack()
                                )
                            }
                        )
                        await dispatcher.feed_update(bot, new_event_update)
                        return
            case InputResult.ERROR:
                question = form_.next()
                if question is not None:
                    await state.set_state(Form.ask)
                    text = f"{form_.error}\n\n" \
                           f"{question.label}\n\n{question.description}"
                    # text = "Ошибка, попробуй ввести ответ как\\-то иначе\\!\n\n" \
                    #        f"*{question.label}*\n\n{question.description}"
                else:
                    await state.set_state(Form.finish)
                    text = "Форма заполнена\\! InputResult\\.ERROR"
            # case InputResult.NOTHING:
            #     await state.set_state(Form.finish)
            #     text = "Форма заполнена\\!"
            case _:
                await state.set_state(Form.finish)
                text = "Форма заполнена\\!"
        keyboard = form_keyboard(form_)
    except BaseException as e:
        print(f"@form_router.message `form_answer` error: {e}")
        await state.set_state(Form.finish)
        text = strings.base().something_went_wrong
        keyboard = None

    await message.answer(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )
