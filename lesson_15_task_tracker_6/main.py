from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Задача 1", "is_complete": False},
    {"id": 2, "title": "Задача 2", "is_complete": True},
]

global_task_id = 2


class InputTask(BaseModel):
    title: str
    is_complete: bool


@app.get("/api/tasks")
def get_tasks():
    return tasks


@app.get("/api/tasks/{id}")
def get_task_by_id(id: int):
    for task in tasks:
        if task["id"] == id:
            return task


@app.post("/api/tasks")
def add_new_task(data: InputTask):
    global global_task_id
    global_task_id += 1

    tasks.append(
        {"id": global_task_id, "title": data.title, "is_complete": data.is_complete}
    )
