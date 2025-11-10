from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import AsyncSessionLocal


async def get_db_session() -> AsyncSession:
    """Зависимость для предоставления асинхронной сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session