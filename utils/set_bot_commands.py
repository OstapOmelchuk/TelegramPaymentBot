from aiogram.types import BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("start", "Start CryptoStellarBot"),
        BotCommand("help", "Help"),
        BotCommand("profile", "Profile"),
        BotCommand("info", "About Private Community"),
        BotCommand("buy_subscription", "Subscribe to CryptoStellar Private"),
    ])
