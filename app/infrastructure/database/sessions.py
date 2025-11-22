from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import AsyncSessionLocal
from typing import AsyncGenerator


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
