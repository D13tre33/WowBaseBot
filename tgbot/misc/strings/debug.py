from tgbot.misc.singleton import Singleton
from aiogram.fsm.state import State


class Debug(Singleton):

    @staticmethod
    def navigation(
            prev_state: str,
            next_state: State,
            result_state: str
    ):
        return f"{prev_state} -> {next_state.state.title()} = {result_state}" \
            .replace("-", "\\-").replace(">", "\\>").replace("_", "\\_").replace("{", "\\") \
            .replace("}", "\\}").replace("=", "\\=")
