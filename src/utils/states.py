from aiogram.dispatcher.filters.state import StatesGroup, State


class MainState(StatesGroup):
    add_data = State()
    remove_data = State()
