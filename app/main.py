from infrastructure.database.connection import (
    create_db_and_tables,
    AsyncSessionLocal,
)
from fastapi import FastAPI

from contextlib import asynccontextmanager

from presentation.api.v1.routers.auth_routers import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается. Создаем базу данных...")
    await create_db_and_tables()
    print("База данных инициализирована.")
    yield
    print("Приложение завершает работу.")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

