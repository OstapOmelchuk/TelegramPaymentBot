from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileRegistration(StatesGroup):
    fullname = State()
    mail = State()
    phone = State()
