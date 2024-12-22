from fastapi import APIRouter
from typing import List
import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title="1つ目のTODOタスク")]


@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.model_dump()) # task_bodyにidを追加して返す


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.model_dump())

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return
