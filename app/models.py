from sqlalchemy import Column, String, DateTime,  Integer
from datetime import datetime
from app.db import Base


class User(Base):
    __tablename__ = "user"

    tg_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class File(Base):
    __tablename__ = "file"

    filehash = Column(String(64), primary_key=True, nullable=False)
    filename = Column(String, unique=True, nullable=False)
    filepath = Column(String, unique=True, nullable=False)
    time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"{self.filename}"
