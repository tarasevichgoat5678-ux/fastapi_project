from sqlite3 import IntegrityError

from database import new_session, TaskOrm, OwnerOrm
from schemas import Taskadd, Task, Owneradd, Owner
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
            except IntegrityError as e:
                if "UNIQUE constraint failed: tasks.id" in str(e):
                    raise ValueError(f"Task with id {data.id} already exists")
                else:
                    raise e

    @classmethod
    async def find_all(cls) -> list[Task]:
        async with new_session() as session:
            qwery = select(TaskOrm)
            result = await session.execute(qwery)
            tasks_models = result.scalars().all()
            return [Task.model_validate(task_model.__dict__) for task_model in tasks_models]



class OwnerRepository:
    @classmethod
    async def add_one(cls, data: Owneradd):
        async with new_session() as session:
            owner_dict = data.model_dump()

            owner = OwnerOrm(**owner_dict)
            session.add(owner)
            await session.flush()
            await session.commit()
            return owner.id

    @classmethod
    async def find_all(cls) -> list[Owner]:
        async with (new_session() as session):
            query = select(OwnerOrm)
            result = await session.execute(query)
            owner_models= result.scalars().all()
            return [Owner.model_validate(owner_model.__dict__) for owner_model in owner_models]

    @classmethod
    async def find_one(cls, owner_id: int) -> Owner:
        async with new_session() as session:
            query = select(OwnerOrm).where(OwnerOrm.id == owner_id)
            result = await session.execute(query)
            owner_orm = result.scalar_one_or_none()
            if owner_orm is None:
                raise ValueError("Owner not found")
            return Owner.model_validate(owner_orm.__dict__)