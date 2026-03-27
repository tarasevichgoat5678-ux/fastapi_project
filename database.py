
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

from config import popa

engine = create_async_engine(popa.PUT)

new_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None ]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
