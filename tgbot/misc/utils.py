from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest


async def check_user_admin_permissions(bot: Bot, user_id: int, chat_id: str) -> bool:
    try:
        chat_administrators = await bot.get_chat_administrators(chat_id=chat_id)
        user_is_admin = False

        for member in chat_administrators:
            if member.user.id == user_id:
                user_is_admin = True
                break

        return user_is_admin
    except TelegramForbiddenError as e:  # aiogram.exceptions.TelegramForbiddenError:
        # Telegram server says Forbidden: bot was kicked from the channel chat
        print("TelegramForbiddenError")
        print(e)
        print(e.message)
        print(e.__traceback__)
        return False
    except TelegramBadRequest as e:
        # Telegram server says Bad Request: member list is inaccessible
        print("TelegramBadRequest")
        print(e)
        print(e.message)
        print(e.__traceback__)
        return False
    except BaseException as e:
        print("BaseException")
        print(e)
        print(e.__traceback__)
        return False


async def check_bot_admin_permissions(bot: Bot, chat_id: str) -> bool:
    bot_chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
    return bot_chat_member.can_manage_chat
