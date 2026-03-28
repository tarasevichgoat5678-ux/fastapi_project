from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from repository import TaskRepository, OwnerRepository, CategoryRepository
from schemas import Taskadd, Task, TaskId, Owner, OwnerAdd, CategoryAdd, Category

router_task = APIRouter(prefix="/tacks", tags=["Таски"])


@router_task.post("", response_model=TaskId, description="Создать задачу")
async def add_task(
        task: Annotated[Taskadd, Depends()],
) -> TaskId:
    try:
        task_id = await TaskRepository.add_one(task)
        return TaskId(task_id=task_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router_task.get("", response_model=list[Task], description="Показать задачи")
async def get_tasks() -> list[Task]:
    tasks = await TaskRepository.find_all()
    return tasks


router_owners = APIRouter(prefix="/owners", tags=["Владельцы"])


@router_owners.post("", response_model=Owner, description="Добавить пользователя")
async def add_owner(
        owner: Annotated[OwnerAdd, Depends()],
) -> Owner:
    owner_id = await OwnerRepository.add_one(owner)
    return Owner(id=owner_id, **owner.model_dump())


@router_owners.get("", response_model=list[Owner], description="Показать всех пользователей")
async def get_owners() -> list[Owner]:
    return await OwnerRepository.find_all()


@router_owners.get("/{owner_id}", response_model=Owner, description="Показать одного пользователя")
async def get_owner(owner_id: int) -> Owner:
    return await OwnerRepository.find_one(owner_id)


router = APIRouter(prefix="/categories", tags=["Категории"])


@router.post("", response_model=Category, description="Создать категорию")
async def add_category(
        category: CategoryAdd,
) -> Category:
    category_id = await CategoryRepository.add_one(category)
    return Category(id=category_id, name=category.name)


@router.get("", response_model=list[Category], description="Показать категории")
async def get_categories() -> list[Category]:
    return await CategoryRepository.find_all()
