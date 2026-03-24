from pydantic import BaseModel


class STackadd(BaseModel):
    name: str
    description: str | None = None


class STack(STackadd):
    id: int


class STackId(BaseModel):
    ok: bool = True
    task_id: int