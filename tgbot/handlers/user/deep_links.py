from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from tgbot.handlers.user.utils import UserRouter
from tgbot.misc.regex import Regex
from tgbot.misc.storage.storage import Storage
from tgbot.misc.strings import strings
from tgbot.models.user import user

deep_links_router = UserRouter()


@deep_links_router.message(Command(Regex.deep_link))
@deep_links_router.message(CommandStart())
async def user_start(message: Message):
    message_text_list = message.text.split(" ")

    deep_link_hash = message_text_list[1] if len(message_text_list) > 1 else None

    payload = decode_payload(deep_link_hash) if deep_link_hash else None

    payload_definition_key = payload.split("-")[0] if payload else None

    text = strings.base().deep_link_welcome_message

    keyboard = None

    await Storage.users.add(user(
        id=message.chat.id,
        username=message.chat.username,
        first_name=message.chat.first_name,
        last_name=message.chat.last_name,
        location=message.chat.location,
    ))

    if await Storage.deep_links.check_existence(payload):
        match payload_definition_key:
            case "aa":
                await Storage.deep_links.remove(payload)
                user_strings = strings.admins()
                text += f"\n\n{user_strings.welcome_admin_action_message}\n\n"
                exists = await Storage.admins.add_id(message.chat.id)
                if not exists:
                    text += user_strings.welcome_admin_success_message
                else:
                    text += user_strings.welcome_admin_exists_message

    await message.answer(
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )
