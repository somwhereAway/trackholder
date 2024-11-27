from sqlalchemy import (
    Column,
    String,
    DateTime,
    BigInteger,
    ForeignKey,
    Boolean,
    Integer,
    UniqueConstraint,
    Table
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.db import Base

MAX_USERNAME_LENGTH = 150


file_customtag_association = Table(
    "file_customtag",
    Base.metadata,
    Column("file_id", String(64), ForeignKey(
        "file.filehash", ondelete="CASCADE"), primary_key=True),
    Column("customtag_id", Integer, ForeignKey(
        "customtag.id", ondelete="CASCADE"), primary_key=True),
)

file_globaltag_association = Table(
    "file_globaltag",
    Base.metadata,
    Column("file_id", String(64), ForeignKey(
        "file.filehash", ondelete="CASCADE"), primary_key=True),
    Column("globaltag_id", Integer, ForeignKey(
        "globaltag.id", ondelete="CASCADE"), primary_key=True),
)


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

    filehash = Column(String(64), primary_key=True, nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, unique=True, nullable=False)
    time = Column(DateTime, default=func.now())
    created_by = Column(BigInteger, ForeignKey(
        "telegram_user.tg_id", ondelete="SET NULL"), nullable=True)
    created_user = relationship(
        "TelegramUser", backref="files", uselist=False, passive_deletes=True)
    customtags = relationship(
        "CustomTag",
        secondary=file_customtag_association,
        back_populates="files",
    )
    globaltags = relationship(
        "GlobalTag",
        secondary=file_globaltag_association,
        back_populates="files",
    )

    def __repr__(self):
        return f"{self.filename}"


class CustomTag(Base):
    __tablename__ = "customtag"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    author = Column(
        BigInteger,
        ForeignKey("telegram_user.tg_id", ondelete="SET NULL"),
        nullable=True
    )
    author_user = relationship(
        "TelegramUser",
        backref="customtags",
        uselist=False,
        passive_deletes=True
    )
    files = relationship(
        "File",
        secondary=file_customtag_association,
        back_populates="customtags",
    )
    __table_args__ = (
        UniqueConstraint('name', 'author', name='uix_name_author'),
    )

    def __repr__(self):
        return f"{self.name}"


class GlobalTag(Base):
    __tablename__ = "globaltag"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    files = relationship(
        "File",
        secondary=file_globaltag_association,
        back_populates="globaltags",
    )

    def __repr__(self):
        return f"{self.name}"
