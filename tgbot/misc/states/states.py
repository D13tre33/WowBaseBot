from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start = State()
    ask = State()
    finish = State()
    submit = State()


class Navigator(StatesGroup):
    idle = State()
    main = State()
    admins = State()
    admins_list = State()
    add_admin = State()
    remove_admin = State()
