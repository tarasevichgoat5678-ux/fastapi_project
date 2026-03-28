from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from repository import TaskRepository, OwnerRepository
from schemas import Taskadd, Task, TaskId, Owner, Owneradd, CategoryAdd

router = APIRouter(prefix="/categories", tags=["Категории"])


@router.post("", response_model=TaskId)
async def add_task(
        task: Annotated[Taskadd, Depends()],
) -> TaskId:
    try:
        task_id = await TaskRepository.add_one(task)
        return TaskId(task_id=task_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=list[Task])
async def get_tasks() -> list[Task]:
    tasks = await TaskRepository.find_all()
    return tasks


@router.post("/owners")
async def add_owner(owner: Annotated[Owneradd, Depends()]) -> None:
    await OwnerRepository.add_one(owner)



@router.get("/owners/{owner_id}", response_model=Owner)
async def get_owner(owner_id: int) -> Owner:
    owner = await OwnerRepository.find_one(owner_id)
    return owner

@router.get("/owners", response_model=list[Owner])
async def get_owners() -> list[Owner]:
    owners = await OwnerRepository.find_all()
    return owners


@router.post("", response_model=CategoryAdd)
async def add_category(category: CategoryAdd) -> CategoryAdd:
    return CategoryAdd(name=category.name)