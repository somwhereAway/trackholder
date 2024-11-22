from sqlalchemy import update
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


async def get_file_by_filepath(filepath: str) -> File:
    async with AsyncSessionLocal() as session:
        statement = select(File).where(File.filepath == filepath)
        result = await session.execute(statement)
        file = result.scalars().first()
        return file


async def get_user_all_file_paths_names(tg_id: int) -> list[tuple[str, str]]:
    async with AsyncSessionLocal() as session:
        statement = select(File).where(File.created_by == tg_id)
        result = await session.execute(statement)
        filepaths_names = [(file.filepath, file.filename)
                           for file in result.scalars().all()]
        return filepaths_names


async def get_all_file_paths_names() -> list[tuple[str, str]]:
    async with AsyncSessionLocal() as session:
        statement = select(File)
        result = await session.execute(statement)
        filepaths_names = [(file.filepath, file.filename)
                           for file in result.scalars().all()]
        return filepaths_names


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


async def is_user_registered(tg_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.tg_id == tg_id)
        )
        return result.scalar_one_or_none()


async def is_superuser(tg_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.tg_id == tg_id)
        )
        user: TelegramUser = result.scalar_one_or_none()
        if user:
            return user.superuser
        return False


async def file_exists_in_database(filehash: int) -> bool | str:
    async with AsyncSessionLocal() as session:
        statement = select(File).where(File.filehash == str(filehash))
        result = await session.execute(statement)
        file: File = result.scalars().first()
        if file is not None:
            return file.filepath
        return False


async def delete_user(tg_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
            return True
        else:
            return False


async def get_all_users() -> list[TelegramUser]:
    async with AsyncSessionLocal() as session:
        statement = select(TelegramUser)
        result = await session.execute(statement)
        return result.scalars().all()


async def get_user(tg_id: int) -> TelegramUser:
    async with AsyncSessionLocal() as session:
        statement = select(TelegramUser).where(TelegramUser.tg_id == tg_id)
        result = await session.execute(statement)
        return result.scalars().first()


async def update_user(tg_id: int, updates: dict) -> bool:
    """
    Обновляет пользователя в базе данных.

    :param tg_id: Telegram ID пользователя
    :param updates: Словарь с полями для обновления
    :return: True, если обновление прошло успешно, False в случае ошибки
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                stmt = (
                    update(TelegramUser)
                    .where(TelegramUser.tg_id == tg_id)
                    .values(**updates)
                )
                result = await session.execute(stmt)
                if result.rowcount == 0:
                    return False

                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                print(f"Ошибка при обновлении пользователя: {e}")
                return False
