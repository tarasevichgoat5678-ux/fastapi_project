from datetime import datetime

from pydantic import BaseModel


class Taskadd(BaseModel):
    name: str
    description: str | None = None
    status: str = 'active'
    create_at: datetime = datetime.now()
    owner_id: int
    category_id: int | None



class Task(Taskadd):
    id: int


class Owneradd(BaseModel):
    name: str
    category_id: int | None = None


class Owner(Owneradd):
    id: int


class TaskId(BaseModel):
    ok: bool = True
    task_id: int


class CategoryAdd(BaseModel):
    name: str
