from aiogram.dispatcher.filters.state import StatesGroup, State


class USDT_TRC20_Payment(StatesGroup):
    TxID = State()
