from fastapi import FastAPI, APIRouter
import logging

from contextlib import asynccontextmanager

from config import Config_put
from database import create_tables, delete_tables
from router import router as tasks_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    logger.info('База очищена')
    await create_tables()
    logger.info('База готова')
    yield
    logger.info('Выключение')


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
