from sqlalchemy.future import select

from app.db import AsyncSessionLocal
from app.models import File


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


async def get_all_files() -> list[File]:
    async with AsyncSessionLocal() as session:
        statement = select(File)
        result = await session.execute(statement)
        files = result.scalars().all()
        return files
