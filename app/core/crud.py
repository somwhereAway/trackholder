from sqlalchemy.future import select

from core.db import AsyncSessionLocal
from core.models import File, TelegramUser


async def create_file(
        file_data: dict
) -> File:
    file = File(**file_data)
    async with AsyncSessionLocal() as session:
        statement = select(File).where(File.filehash == file_data['filehash'])
        result = await session.execute(statement)
        file_from_db = result.scalars().first()
        if file_from_db:
            return False
        session.add(file)
        await session.commit()
        await session.refresh(file)
    return file


async def get_file(filehash: str) -> File:
    async with AsyncSessionLocal() as session:
        statement = select(File).where(File.filehash == filehash)
        result = await session.execute(statement)
        file = result.scalars().first()
        return file


async def get_user_all_file_paths(tg_id: int) -> list[str]:
    async with AsyncSessionLocal() as session:
        statement = select(File).where(File.created_by == tg_id)
        result = await session.execute(statement)
        filepaths = [file.filepath for file in result.scalars().all()]
        return filepaths


async def get_or_create_telegram_user(tg_id, first_name, last_name, username):
    created = False
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.tg_id == tg_id)
        )
        telegram_user = result.scalar_one_or_none()

        if telegram_user is None:
            telegram_user = TelegramUser(
                tg_id=tg_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            session.add(telegram_user)
            await session.commit()
            created = True
            await session.refresh(telegram_user)

    return telegram_user, created
