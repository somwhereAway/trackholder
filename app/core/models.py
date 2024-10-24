from sqlalchemy import (
    Column, String, DateTime, Integer, ForeignKey, Boolean
)
from datetime import datetime,  timezone
from core.db import Base

MAX_USERNAME_LENGTH = 150


class TelegramUser(Base):
    __tablename__ = "telegram_user"

    tg_id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String(MAX_USERNAME_LENGTH), nullable=False)
    last_name = Column(String(MAX_USERNAME_LENGTH), nullable=True)
    username = Column(String(MAX_USERNAME_LENGTH), nullable=True)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(
        DateTime, default=datetime.now(timezone.utc)
    )
    superuser = Column(Boolean, default=False)
    staff_user = Column(Boolean, default=False)

    def __repr__(self):
        return (f"<TelegramUser(tg_id={self.tg_id}, "
                f"username='{self.username}')>")


class File(Base):
    __tablename__ = "file"

    filehash = Column(String(64), primary_key=True, nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, unique=True, nullable=False)
    time = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey(
        "telegram_user.tg_id"), nullable=True)

    def __repr__(self):
        return f"{self.filename}"
