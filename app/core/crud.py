from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import File, TelegramUser


async def create_file(
        file_data: dict,
        session: AsyncSession
) -> File:
    file = File(**file_data)
    statement = select(File).where(File.filehash == file_data['filehash'])
    result = await session.execute(statement)
    file_from_db = result.scalars().first()
    if file_from_db:
        return False
    session.add(file)
    await session.commit()
    await session.refresh(file)
    return file


async def get_file(filehash: str, session: AsyncSession) -> File:
    statement = select(File).where(File.filehash == filehash)
    result = await session.execute(statement)
    return result.scalars().first()


async def get_file_by_filepath(filepath: str, session: AsyncSession) -> File:
    statement = select(File).where(File.filepath == filepath)
    result = await session.execute(statement)
    return result.scalars().first()


async def get_user_all_file_paths_names(
    tg_id: int,
    session: AsyncSession
) -> list[tuple[str, str]]:
    statement = select(File).where(File.created_by == tg_id)
    result = await session.execute(statement)
    return [(file.filepath, file.filename) for file in result.scalars().all()]


async def get_all_file_paths_names(
        session: AsyncSession) -> list[tuple[str, str]]:
    statement = select(File)
    result = await session.execute(statement)
    return [(file.filepath, file.filename) for file in result.scalars().all()]


async def get_or_create_telegram_user(
    tg_id: int,
    first_name: str,
    last_name: str,
    username: str,
    session: AsyncSession
):
    created = False
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


async def is_user_registered(
    tg_id: int,
    session: AsyncSession
) -> TelegramUser:
    result = await session.execute(
        select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    )
    return result.scalar_one_or_none()


async def is_superuser(tg_id: int, session: AsyncSession) -> bool:
    result = await session.execute(
        select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    )
    user: TelegramUser = result.scalar_one_or_none()
    return user.superuser if user else False


async def file_exists_in_database(
    filehash: int,
    session: AsyncSession
) -> bool | str:
    statement = select(File).where(File.filehash == str(filehash))
    result = await session.execute(statement)
    file: File = result.scalars().first()
    return file.filepath if file else False


async def delete_user(tg_id: int, session: AsyncSession) -> bool:
    result = await session.execute(
        select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    )
    user = result.scalar_one_or_none()
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False


async def get_all_users(session: AsyncSession) -> list[TelegramUser]:
    statement = select(TelegramUser)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_user(tg_id: int, session: AsyncSession) -> TelegramUser:
    statement = select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    result = await session.execute(statement)
    return result.scalars().first()


async def update_user(
    tg_id: int,
    updates: dict,
    session: AsyncSession
) -> bool:
    """
    Обновляет пользователя в базе данных.

    :param tg_id: Telegram ID пользователя
    :param updates: Словарь с полями для обновления
    :param session: Сессия базы данных
    :return: True, если обновление прошло успешно, False в случае ошибки
    """
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
