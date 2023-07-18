from sqlalchemy import Column, BigInteger, String, sql, DateTime

from utils.db_api.db import TimedBaseModel


class Payment(TimedBaseModel):
    __tablename__ = "Payment"
    payment_id = Column(BigInteger, nullable=False, primary_key=True)
    tx_id = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    user_id = Column(BigInteger, nullable=False)

    query: sql.select
