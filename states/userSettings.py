from aiogram.dispatcher.filters.state import StatesGroup, State


class UserSetting(StatesGroup):
    TwitchName = State()
    IsGaming = State()
    CustomBetUser = State()


class AdminSettings(StatesGroup):
    Admin = State()

