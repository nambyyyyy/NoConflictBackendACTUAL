from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from infrastructure.persistence.sqlalchemy.models.user import UserORM
from infrastructure.persistence.sqlalchemy.models.profile import ProfileORM
from infrastructure.persistence.sqlalchemy.models.conflict import ConflictORM
from infrastructure.persistence.sqlalchemy.models.conflict_item import ConflictItemORM
from infrastructure.persistence.sqlalchemy.models.conflict_event import ConflictEventORM
from infrastructure.persistence.sqlalchemy.models.base import Base


DATABASE_URL = "postgresql+asyncpg://no_conflict_user:777555333w@localhost/no_conflict_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db_and_tables():
    print("Таблицы в metadata:", Base.metadata.tables.keys())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)