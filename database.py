from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

from config import polka


class Model(DeclarativeBase):
    pass


class CategoryOrm(Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class CityOrm(Model):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[str] = mapped_column(default="active")
    create_at: Mapped[datetime] = mapped_column(default=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    city: Mapped[str | None]


engine = create_async_engine(polka.PUT)
new_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class OwnerOrm(Model):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
