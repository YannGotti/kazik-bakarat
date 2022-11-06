from aiogram.dispatcher.filters.state import StatesGroup, State


class UserSetting(StatesGroup):
    TwitchName = State()
