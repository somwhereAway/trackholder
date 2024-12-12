import os
from functools import wraps

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
# DATABASE_URL = 'sqlite+aiosqlite:///database.db'

Base = declarative_base()

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


@asynccontextmanager
async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


def with_db_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'session' not in kwargs or kwargs['session'] is None:
            async with get_async_session() as session:
                try:
                    kwargs['session'] = session
                    result = await func(*args, **kwargs)
                    await session.commit()
                    return result
                except Exception as e:
                    await session.rollback()
                    raise e
        else:
            return await func(*args, **kwargs)
    return wrapper
