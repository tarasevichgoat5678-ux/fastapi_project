from database import new_session, TaskOrm
from schemas import STackadd, STack
from sqlalchemy import select



class TaskRepository:
    @classmethod
    async def add_one(cls, data: STackadd):
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STack]:
        async with new_session() as session:
            qwery = select(TaskOrm)
            result = await session.execute(qwery)
            tasks_models = result.scalars().all()
            task_schemas = [STack.model_validate(task_model) for task_model in tasks_models ]
            return task_schemas
