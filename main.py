import asyncio
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()


class Task(BaseModel):
    duration: int


tasks = {}


async def task_worker(task_id, duration):
    await asyncio.sleep(duration)
    tasks[task_id] = 'done'
    return tasks


@app.post("/task", response_model=dict)
async def create_task(task: Task):
    task_id = str(uuid.uuid4())
    task = Task(duration=5)
    tasks[task_id] = "running"
    await asyncio.create_task(task_worker(task_id, task.duration))
    return JSONResponse(content={"task_id": task_id})


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": tasks[task_id]}


