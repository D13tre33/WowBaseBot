import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.bootstrap import bootstrap
from tgbot.config import load_config

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    if config.tg_bot.use_redis:
        db = RedisStorage.from_url(config.redis.dsn(), key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True))
    else:
        db = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode=None)
    dp = Dispatcher(storage=db)

    await bootstrap(config, dp, bot)

    await dp.start_polling(
        bot,
        allowed_updates=[
            "update_id",
            "message",
            "edited_message",
            "channel_post",
            "edited_channel_post",
            "inline_query",
            "chosen_inline_result",
            "callback_query",
            "shipping_query",
            "pre_checkout_query",
            "poll",
            "poll_answer",
            "my_chat_member",
            "chat_member",
            "chat_join_request",
        ]
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот был выключен!")
