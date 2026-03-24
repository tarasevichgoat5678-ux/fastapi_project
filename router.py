from typing import Annotated

from fastapi import APIRouter, Depends

from repository import TaskRepository
from schemas import STackadd, STack, STackId

router = APIRouter(prefix="/tasks", tags=["Таски"])


@router.post("")
async def add_task(
        task: Annotated[STackadd, Depends()],
) -> STackId:
    task_id = await TaskRepository.add_one(task)
    return {'ok': True, "task_id": task_id}


@router.get("", response_model=list[STack])
async def get_tasks() -> list[STack]:
    tasks = await TaskRepository.find_all()
    return tasks
