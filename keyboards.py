from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb = CallbackData("subscription", "price", "type", "name")

subscription_price = "15"

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Subscribe to CryptoStellar Private"),
            KeyboardButton(text="About Private Community")
        ],
        [
            KeyboardButton(text="Profile"),
            KeyboardButton(text="Help"),
        ]
    ],
    resize_keyboard=True
)

subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='USDT (TRC20)',
                                 callback_data=cb.new(price=subscription_price, type="1", name='USDT_TRC20')),
            InlineKeyboardButton(text='USD (PayPal)',
                                 callback_data=cb.new(price=subscription_price, type="2", name='PayPal'))
        ],
        [
            InlineKeyboardButton(text='Back', callback_data='cancel_subscription_payment')
        ]
    ]
)

only_back_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Back', callback_data='back_to_payments')
        ]
    ]
)

go_to_payments_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Buy subscription', callback_data='go_to_payments')
        ]
    ]
)

create_profile_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Create Profile', callback_data='create_profile')
        ]
    ]
)

cancel_profile_creation_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cancel", callback_data='cancel_profile_creation')
        ]
    ]
)

cancel_payment_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cancel", callback_data='cancel_payment')
        ]
    ]
)

profile_creation_finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Activate account", request_contact=True),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
