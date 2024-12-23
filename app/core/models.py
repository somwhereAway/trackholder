from sqlalchemy import (
    Column, String, DateTime, BigInteger, ForeignKey, Boolean
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.db import Base

MAX_USERNAME_LENGTH = 150


class TelegramUser(Base):
    __tablename__ = "telegram_user"

    tg_id = Column(BigInteger, primary_key=True, unique=True)
    first_name = Column(String(MAX_USERNAME_LENGTH), nullable=False)
    last_name = Column(String(MAX_USERNAME_LENGTH), nullable=True)
    username = Column(String(MAX_USERNAME_LENGTH), nullable=True)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(
        DateTime, default=func.now()
    )
    superuser = Column(Boolean, default=False)
    staff_user = Column(Boolean, default=False)

    def __repr__(self):
        return (f"<TelegramUser(tg_id={self.tg_id}, "
                f"username='{self.username}')>")


class File(Base):
    __tablename__ = "file"
    id = Column
    filehash = Column(String(64), primary_key=True, nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, unique=True, nullable=False)
    time = Column(DateTime, default=func.now())
    created_by = Column(BigInteger, ForeignKey(
        "telegram_user.tg_id", ondelete="SET NULL"), nullable=True)
    created_user = relationship(
        "TelegramUser", backref="files", uselist=False, passive_deletes=True)

    def __repr__(self):
        return f"{self.filename}"
