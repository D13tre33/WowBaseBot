from tgbot.misc.singleton import Singleton


class Base(Singleton):
    empty_string_error = "Каким\\-то образом была введена пустая строка \\.\\.\\."

    main_menu = "Главное меню"
    list = "Список"

    cancel = "Отмена"

    support = "Поддержка"

    to_menu = "В меню"
    repeat = "Заново"
    confirm = "Норм"

    in_a_day = "Через сутки"
    in_a_week = "Через неделю"
    in_a_month = "Через месяц"

    title = "Название"
    first_name = "Имя"
    last_name = "Фамилия"
    user_name = "Никнейм"
    location = "Локация"

    text_input_description = "_Ты можешь использовать встроенное форматирование текста\\!_ *\\(Кроме спойлеров\\)*"

    something_went_wrong = "Что\\-то пошло не так \\.\\.\\."

    deep_link_welcome_message = "Добро пожаловать\\!"

    free_action_interpret_error_message = "Не удалось интерпретировать свободное действие \\.\\.\\."
