from infrastructure.database.connection import (
    create_db_and_tables,
    AsyncSessionLocal,
    engine
)
from fastapi import FastAPI

from contextlib import asynccontextmanager

from presentation.api.v1.routers.auth_routers import router as auth_router
from presentation.api.v1.routers.conflict_routers import router as conflict_router
from presentation.api.v1.ws.conflict_ws import router as conflict_ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается. Создаем базу данных...")
    await create_db_and_tables()
    print("База данных инициализирована.")
    yield
    print("Приложение завершает работу.")
    await engine.dispose()



app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(conflict_router, prefix="/api/v1/conflicts", tags=["conflicts"])
app.include_router(conflict_ws_router, prefix="/api/v1/ws/conflict", tags=["conflict_ws"])
