from fastapi import FastAPI, APIRouter
import logging

from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from router import router_task as tasks_router
from router import router as categories_router
from router import router_owners as owners_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await delete_tables()
        logger.info("База очищена")
    except Exception as e:
        logger.error("Ошибка при удалении таблиц: %s", e)
        raise

    try:
        await create_tables()
        logger.info("База готова")
    except Exception as e:
        logger.error("Ошибка при создании таблиц: %s", e)
        raise

    yield  # тут работает приложение

    logger.info("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(owners_router)
app.include_router(categories_router)
