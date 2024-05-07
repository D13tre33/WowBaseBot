from typing import List

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from tgbot.config import Config
from tgbot.handlers.admin.admin import admin_router
from tgbot.handlers.base import base_router
from tgbot.handlers.su.su import su_router
from tgbot.handlers.user.user import user_router
from tgbot.middlewares.config import ConfigMiddleware, DispatcherMiddleware
from tgbot.misc.actions import NavigationAction, NavigatorAction
from tgbot.misc.forms.form import form
from tgbot.misc.forms.inputs.input import text_input, user_id_input
from tgbot.misc.forms.inputs.validators.validator import username_or_id_validator
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings
from tgbot.models.scheduler import Task
from tgbot.services import broadcaster


def register_routers(dp: Dispatcher):
    for router in [
        base_router,
        su_router,
        admin_router,
        user_router,
    ]:
        dp.include_router(router)


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.message.outer_middleware(DispatcherMiddleware(dp))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(DispatcherMiddleware(dp))
    # dp.feed_update()


async def register_forms():
    await Storage.forms.set(form(
        uuid="remove_admin_form",
        # parent_screen="admins",
        callback_title=strings.base().to_menu,
        callback_data=NavigationAction(action=NavigatorAction.navigate, to="admins").pack(),
        label="Удали админа",
        description="",
        inputs=[
            user_id_input(
                name="user_id",
                title="ID админа",
                label=strings.admins().remove_admin_start_message,
                description="",
                error=strings.admins().bad_admin_id_message_format,
                markdown=False
            )
        ]
    ))

    await Storage.forms.set(form(
        uuid="sm",  # send_message
        callback_title=strings.base().to_menu,
        callback_data=NavigationAction(action=NavigatorAction.navigate, to="main").pack(),
        label="*Отправка сообщения*",
        description="",
        inputs=[
            text_input(
                name="username_or_id",
                title="Username или ID",
                label="Отправь мне *@username* или *ID* получателя \\(пользователя или чата\\) \\.\\.\\.",
                description="",
                error="Неверный формат *@username* или *ID* пользователя или чата \\.\\.\\.",
                markdown=False,
                validators=[username_or_id_validator()]
            ),
            text_input(
                name="text",
                title="Текст",
                label="Отправь мне текст сообщения \\.\\.\\.",
                description=strings.base().text_input_description,
                error=strings.base().empty_string_error
            ),
        ]
    ))

    await Storage.forms.set(form(
        uuid="support",
        callback_title=strings.base().to_menu,
        callback_data=NavigationAction(action=NavigatorAction.navigate, to="main").pack(),
        label=strings.base().support,
        description="",
        inputs=[
            text_input(
                name="text",
                title="Текст",
                label="Напиши мне свой вопрос или предложение, а я передам его админам\\!",
                # description="Пока что понимаю только текст \\.\\.\\.",
                description="",
                error=strings.base().empty_string_error,
                markdown=False,
                validators=[]
            )
        ]
    ))


async def on_startup(bot: Bot, admin_ids: List[int], tasks_counter: int):
    await bot.set_my_commands(
        commands=[
            BotCommand(command="menu", description="Открыть главное меню"),
        ]
    )
    await broadcaster.broadcast(
        bot=bot,
        users_ids=admin_ids,
        text=f"Бот запущен!\nВосстановлено задач - {tasks_counter}"
    )


async def bootstrap(config: Config, dp: Dispatcher, bot: Bot):
    register_routers(dp)
    register_global_middlewares(dp, config)

    Storage.init(dp.fsm, bot)

    await register_forms()

    await Storage.admins.set_env_ids(config.tg_bot.admin_ids)
    await Storage.su.set_ids(config.tg_bot.su_ids)

    admin_ids = await Storage.admins.get_ids()

    scheduler = await Storage.scheduler.get()
    tasks: List[Task] = scheduler.get_tasks()

    tasks_counter = 0

    for task in tasks:
        task.set_env(Storage, scheduler, dp, bot)
        is_started = await task.start()
        if is_started:
            tasks_counter += 1

    await on_startup(bot, admin_ids, tasks_counter)
