from datetime import datetime
from dateutil.relativedelta import relativedelta

from asyncpg import UniqueViolationError

from utils.db_api.db import db
from utils.db_api.schemas.user import User, Payment


async def add_user(
        user_id: int,
        fullname: str,
        username: str,
        mail: str,
        phone: str,
        status: str = "active",
        subscription_status: bool = False,
        subscription_start_date=None,
        subscription_end_date=None
):
    try:
        user = User(
            user_id=user_id,
            fullname=fullname,
            username=username,
            mail=mail,
            phone=phone,
            status=status,
            subscription_status=subscription_status,
            subscription_start_date=subscription_start_date,
            subscription_end_date=subscription_end_date
        )
        await user.create()
    except UniqueViolationError:
        print("User was not added")


async def update_user_subscription(user_id):
    try:
        user = await select_user(user_id=user_id)
        user.subscription_status = True
        now = datetime.now()
        one_month_from_now = now + relativedelta(months=1, days=1)

        await User.update.values(
            subscription_status=True,
            subscription_start_date=now,
            subscription_end_date=one_month_from_now
        ).where(User.user_id == user_id).gino.status()

    except UniqueViolationError:
        print(f"User with id {user_id} was not found")


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def create_transaction(tx_id: int, username: str, user_id: int):
    try:
        transaction = Payment(
            tx_id=tx_id, username=username, user_id=user_id
        )
        await transaction.create()
    except UniqueViolationError:
        print("Transaction was not added")


async def select_transaction(tx_id: str):
    transaction = await Payment.query.where(Payment.tx_id == tx_id).gino.first()
    return transaction
