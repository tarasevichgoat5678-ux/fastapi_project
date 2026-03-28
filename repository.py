from sqlite3 import IntegrityError

from fastapi import HTTPException

from database import new_session, TaskOrm, OwnerOrm, CategoryOrm
from schemas import Taskadd, Task, Owner, OwnerAdd, CategoryAdd, Category
from sqlalchemy import select


class TaskRepository:
    @classmethod
    async def add_one(cls, data: Taskadd) -> int:
        async with new_session() as session:
            try:
                task = TaskOrm(**data.model_dump())
                session.add(task)
                await session.flush()
                await session.commit()
                return task.id
            except IntegrityError:
                raise HTTPException(status_code=409,detail="Task with such constraints already exists")

    @classmethod
    async def find_all(cls) -> list[Task]:
        async with new_session() as session:
            qwery = select(TaskOrm)
            result = await session.execute(qwery)
            tasks_models = result.scalars().all()
            return [Task.model_validate(task_model.__dict__) for task_model in tasks_models]


class OwnerRepository:
    @classmethod
    async def add_one(cls, data: OwnerAdd):
        async with new_session() as session:
            try:
                owner_dict = data.model_dump()
                owner = OwnerOrm(**owner_dict)
                session.add(owner)
                await session.flush()
                await session.commit()
                return owner.id
            except IntegrityError:
                raise HTTPException(status_code=409,detail="Owner with such constraints already exists")

    @classmethod
    async def find_all(cls) -> list[Owner]:
        async with (new_session() as session):
            query = select(OwnerOrm)
            result = await session.execute(query)
            owner_models = result.scalars().all()
            return [Owner.model_validate(owner_model.__dict__) for owner_model in owner_models]

    @classmethod
    async def find_one(cls, owner_id: int) -> Owner:
        async with new_session() as session:
            query = select(OwnerOrm).where(OwnerOrm.id == owner_id)
            result = await session.execute(query)
            owner_orm = result.scalar_one_or_none()
            if owner_orm is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Owner with id={owner_id} not found"
                )
            return Owner.model_validate(owner_orm.__dict__)


class CategoryRepository:
    @classmethod
    async def add_one(cls, data: CategoryAdd) -> int:
        async with new_session() as session:
            try:
                category = CategoryOrm(**data.model_dump())
                session.add(category)
                await session.flush()
                await session.commit()
            except IntegrityError:
                raise HTTPException(
                    status_code=409,
                    detail="Category with such name already exists"
                )


    @classmethod
    async def find_all(cls) -> list[Category]:
        async with new_session() as session:
            query = select(CategoryOrm)
            result = await session.execute(query)
            orm_cats = result.scalars().all()
            return [Category.model_validate(t.__dict__) for t in orm_cats]
