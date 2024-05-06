from tgbot.misc.singleton import Singleton
from tgbot.models.actions import SendMessageAction
from tgbot.misc.strings.escape import escape
from tgbot.models.support import Support
from tgbot.models.user import User


class Actions(Singleton):
    send_message = "Отправить сообщение"

    @staticmethod
    def message_sent_success(send_message_action_: SendMessageAction):
        return (f"*Сообщение успешно отправлено\\!*"
                f"\n\nПолучатель \\- *{escape(send_message_action_.username_or_id)}*"
                f"\n\n{send_message_action_.text}")

    @staticmethod
    def message_sent_chat_not_found_error(send_message_action_: SendMessageAction):
        if send_message_action_.username_or_id.startswith("@"):
            text = (f"Пользователь или чат с юзернеймом *{escape(send_message_action_.username_or_id)}* не найден\\!"
                    f"\n\nМожно попробовать использовать *ID* \\.\\.\\.")
        else:
            text = (f"Пользователь или чат с ID *`{escape(send_message_action_.username_or_id)}`* не найден\\!"
                    f"\n\nСудя по всему, у бота нет переписки с этим пользователем или он не добавлен в чат, "
                    f"можно повторить попытку позже или написать лично \\.\\.\\.")
        return text

    support = "Поддержка"

    @staticmethod
    def support_message(support_: Support, user_: User):
        return "*Новое обращение в поддержку*\n\n" \
                f"*ID* \\- `{user_.id}`\n" \
                f"*Username* \\- @{escape(user_.username)}\n\n" \
                f"{escape(support_.text)}"

    @staticmethod
    def support_message_sender_info(user_: User):
        return "*Новое обращение в поддержку*\n\n" \
                f"*ID* \\- `{user_.id}`\n" \
                f"*Username* \\- @{escape(user_.username)}\n\n"
