import logging
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher.filters import Text
from keyboards import subscription_keyboard, start_keyboard, only_back_key, go_to_payments_key, create_profile_key, \
    cancel_profile_creation_key, cb, profile_creation_finish_keyboard, cancel_payment_key
from aiogram.dispatcher import FSMContext
from main import dp
from utils.db_api import quick_db_commands as commands
from states.profile_registration import ProfileRegistration
from states.payments_state import USDT_TRC20_Payment
from utils.text_responses import usdt_trc20_payment_info, private_community_info
from utils.validations import is_valid_email, is_valid_full_name
from tronapi import Tron
from config import WADRESS, SUB_COST

tron = Tron()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_valid_transaction(tx_ID):
    try:
        transaction = tron.trx.get_transaction(tx_ID)
        if transaction["ret"][0]["contractRet"] == "SUCCESS":
            contract_data = transaction["raw_data"]["contract"][0]["parameter"]["value"]

            data = contract_data["data"]
            recipient_address_hex = data[32:72]
            transfer_amount_hex = data[72:136]
            transfer_amount = int(transfer_amount_hex, 16) / 1_000_000

            recipient_address = tron.address.from_hex('41' + recipient_address_hex)
            if recipient_address.decode('utf-8') == WADRESS:
                if transfer_amount >= SUB_COST:
                    return {"result": True, "message": ""}
                return {"result": False,
                        "message": "You have transferred an insufficient amount of money."
                                   "\nIf there is a mistake, please write to support (/help) or enter another TxID."}

            return {
                "result": False,
                "message": "This transaction was transferred to an incorrect wallet address."
                           "\nYou may have copied a wrong txID."
            }

        return {"result": False, "message": "Wrong TxID (Transaction with this TxID does not exist)."}
    except Exception as e:
        logger.info(e)
        return {"result": False, "message": "Wrong TxID (Transaction with this TxID does not exist)."}


async def try_buy_subscription(message: Message, is_callback=False):
    if is_callback:
        user_id = message.chat.id
    else:
        user_id = message.from_user.id
    try:
        user = await commands.select_user(user_id)
        if user.status == "active" and not user.subscription_status:
            await message.answer(text='Choose payment method:', reply_markup=subscription_keyboard)
        elif user.status == "banned":
            await message.answer(f"{message.from_user.username}, You are banned.")
        elif user.subscription_status:
            await message.answer(
                f"You are already subscribed."
                f"\nYour subscription will expire on <b>{user.subscription_end_date.strftime('%Y-%m-%d')}</b> 🗓"
            )
    except Exception:
        await message.answer(
            "You need to create profile (register) first.",
            reply_markup=create_profile_key
        )


async def on_startup(dp):
    from utils.db_api.db import on_startup
    await on_startup(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print("bot has been started its work.")


@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer(text="Hello, dear friend!", reply_markup=start_keyboard)


@dp.message_handler(Text(equals=["About Private Community"]))
@dp.message_handler(commands=["info"])
async def get_community_info(message: Message):
    await message.answer(private_community_info, reply_markup=go_to_payments_key)


@dp.message_handler(Text(equals=["Help"]))
@dp.message_handler(commands=["help"])
async def get_help_message(message: Message):
    await message.answer(
        "❓💭 If you have any problems or questions, please contact our manager:\n\n https://t.me/OstapOmelchuk"
    )


@dp.message_handler(Text(equals=["Subscribe to CryptoStellar Private"]))
@dp.message_handler(commands=["buy_subscription"])
async def profile_data(message: Message):
    await try_buy_subscription(message)


@dp.message_handler(Text(equals=["Profile"]))
@dp.message_handler(commands=["profile"])
async def profile_data(message: Message):
    try:
        user = await commands.select_user(message.from_user.id)
        if user and user.status == "active":

            subscription_info = f"\nsubscription start - {user.subscription_start_date.strftime('%Y-%m-%d')}\n" \
                                f"subscription end - {user.subscription_end_date.strftime('%Y-%m-%d')}\n" \
                if user.subscription_status == True else ""
            await message.answer(f"Hello, {user.fullname} 👋\n\n"
                                 f"💬 Here's You profile data:\n\n"
                                 f"<b>ID</b> - {user.user_id}\n"
                                 f"<b>fullname</b> - {user.fullname}\n"
                                 f"<b>mail</b> - {user.mail}\n"
                                 f"<b>phone</b> - {user.phone}\n"
                                 f"<b>username</b> - @{user.username}\n"
                                 f"<b>subscription status</b> - {'active' if user.subscription_status == True else 'not active'}" +
                                 subscription_info
                                 )
        elif user and user.status:
            await message.answer(f"You are banned.")
    except Exception as e:
        logger.info(e)
        await message.answer(
            "You don't have a profile yet. Do You want to create it?",
            reply_markup=create_profile_key
        )


@dp.callback_query_handler(Text(equals='create_profile'), state=None)
async def create_profile(callback: CallbackQuery):
    await callback.message.answer(
        f"Enter your full name:", reply_markup=cancel_profile_creation_key
    )
    await ProfileRegistration.fullname.set()


@dp.message_handler(lambda message: not is_valid_full_name(message.text), state=ProfileRegistration.fullname)
async def invalid_full_name(message: Message):
    await message.answer("Full name is not valid. Please try again.", reply_markup=cancel_profile_creation_key)


@dp.message_handler(lambda message: is_valid_full_name(message.text), state=ProfileRegistration.fullname)
async def get_full_name_to_register(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Now enter your mail, please:", reply_markup=cancel_profile_creation_key)
    await ProfileRegistration.mail.set()


@dp.message_handler(lambda message: not is_valid_email(message.text), state=ProfileRegistration.mail)
async def invalid_email(message: Message):
    await message.answer("Email is not valid. Please try again.", reply_markup=cancel_profile_creation_key)


@dp.message_handler(lambda message: is_valid_email(message.text), state=ProfileRegistration.mail)
async def get_mail_to_register(message: Message, state: FSMContext):
    await state.update_data(mail=message.text)
    await message.answer(
        f"To make your account active, you need to verify it with your phone number.",
        reply_markup=profile_creation_finish_keyboard
    )
    await message.answer(
        f"Press the 'Activate account' button to finish profile creation.",
        reply_markup=cancel_profile_creation_key
    )
    await ProfileRegistration.phone.set()


@dp.message_handler(content_types=[ContentType.CONTACT], state=ProfileRegistration.phone)
async def get_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    await commands.add_user(
        user_id=message.from_user.id,
        fullname=data['fullname'],
        username=message.from_user.username,
        mail=data['mail'],
        phone=data['phone']
    )

    await message.answer(f"You are successfully registered!\n\n"
                         f"<b>Your profile data:</b>\n\n"
                         f"<b>ID</b> - {message.from_user.id}\n"
                         f"<b>fullname</b> - {data['fullname']}\n"
                         f"<b>mail</b> - {data['mail']}\n"
                         f"<b>phone</b> - {data['phone']}\n"
                         f"<b>username</b> - @{message.from_user.username}\n"
                         f"<b>subscription status</b> - not active",
                         reply_markup=start_keyboard)

    await state.finish()


@dp.callback_query_handler(cb.filter(type="1"), state=None)
async def usdt_subscription(callback: CallbackQuery):
    await callback.message.edit_text(usdt_trc20_payment_info, reply_markup=cancel_payment_key)
    await USDT_TRC20_Payment.TxID.set()


@dp.message_handler(state=USDT_TRC20_Payment.TxID)
async def invalid_TxID(message: Message, state: FSMContext):
    is_tx_valid = is_valid_transaction(message.text)
    if is_tx_valid["result"]:
        try:
            transaction = await commands.select_transaction(message.text)
            if transaction:
                await message.answer(
                    "This TxID has already been used to confirm a transaction before. "
                    "\nIf there is a mistake, please write to support (click 'Help' button in the main menu).",
                    reply_markup=cancel_payment_key
                )
            else:
                await state.update_data(TxID=message.text)
                data = await state.get_data()
                await commands.create_transaction(
                    tx_id=data["TxID"],
                    username=message.from_user.username,
                    user_id=message.from_user.id
                )
                await commands.update_user_subscription(message.from_user.id)
                await message.answer(f"Thank you and welcome to our community!!!\n"
                                     f"Here's the link to our private chat: \n\n"
                                     f"https://t.me/+6Mf2Ia4GPSQ5MmEy\n"
                                     f"https://t.me/+6Mf2Ia4GPSQ5MmEy\n"
                                     f"https://t.me/+6Mf2Ia4GPSQ5MmEy\n\n"
                                     f"Now you are one of us.")
                await state.finish()
                logger.info(f"{message.from_user.username} subscribed for private community.")

        except Exception as e:
            logger.info(f"Error - {e}")

    else:
        await message.answer(
            is_tx_valid["message"],
            reply_markup=cancel_payment_key
        )


@dp.callback_query_handler(cb.filter(type="2"))
async def paypal_subscription(callback: CallbackQuery):
    await callback.message.answer(f"Тут буде інструкція і подальша логіка оплати для PayPal",
                                  reply_markup=only_back_key)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(Text(equals='cancel_profile_creation'),
                           state=[ProfileRegistration.fullname, ProfileRegistration.mail, ProfileRegistration.phone])
async def cancel_profile_creation_action(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer("canceled")
    await call.message.answer("profile creation was canceled", reply_markup=start_keyboard)


@dp.callback_query_handler(Text(equals='cancel_payment'),
                           state=[USDT_TRC20_Payment.TxID])
async def cancel_payment_action(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.answer("canceled")
    await call.message.answer("Payment was canceled")


@dp.callback_query_handler(Text(equals='go_to_payments'))
async def cancel(call: CallbackQuery):
    await call.answer("subscriptions")
    await try_buy_subscription(call.message, True)


@dp.callback_query_handler(Text(equals='cancel_subscription_payment'))
async def cancel_subscription_payment(call: CallbackQuery):
    await call.answer("canceled")
    await call.message.edit_text("Action was canceled")


@dp.callback_query_handler(Text(equals='back_to_payments'))
async def back_to_payments(call: CallbackQuery):
    await call.answer("canceled")
    await call.message.edit_text("Choose payment method:", reply_markup=subscription_keyboard)


def is_Cancel_or_Back_btn(c):
    btn_text = c.message.reply_markup.inline_keyboard[0][0].text
    if btn_text.lower() in ["cancel", "back"]:
        return True
    return False


@dp.callback_query_handler(lambda c: is_Cancel_or_Back_btn(c))
async def process_callback_button1(call: CallbackQuery):
    await call.message.delete()
