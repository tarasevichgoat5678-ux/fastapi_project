from datetime import datetime

from pydantic import BaseModel


class Taskadd(BaseModel):
    name: str
    description: str | None = None
    status: str = 'active'
    owner_id: int
    category_id: int | None = None
    city: str | None = None


class Task(Taskadd):
    id: int
    create_at: datetime


class OwnerAdd(BaseModel):
    name: str


class Owner(OwnerAdd):
    id: int


class TaskId(BaseModel):
    ok: bool = True
    task_id: int


class CategoryAdd(BaseModel):
    name: str


class Category(CategoryAdd):
    id: int | None
