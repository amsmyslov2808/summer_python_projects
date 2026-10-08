"""Простой CRUD API без базы данных.

Все задачи хранятся в списке tasks и пропадают после перезапуска сервера.
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Простой Task Tracker API")

# Клиент запускается отдельно через Live Server на порту 5500.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    is_complete: bool


# Это временное хранилище в оперативной памяти, а не база данных.
tasks = [
    {"id": 1, "title": "Изучить GET", "is_complete": True},
    {"id": 2, "title": "Попробовать POST в Postman", "is_complete": False},
]
next_task_id = 3


def find_task(task_id: int):
    """Находит задачу по id или возвращает ошибку 404."""

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.get("/api/tasks")
def get_tasks():
    """READ: возвращает все задачи."""

    return tasks


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    """READ: возвращает одну задачу по её id."""

    return find_task(task_id)


@app.post("/api/tasks", status_code=201)
def create_task(data: TaskCreate):
    """CREATE: добавляет новую задачу."""

    global next_task_id

    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Название не может быть пустым")

    new_task = {
        "id": next_task_id,
        "title": title,
        "is_complete": False,
    }
    tasks.append(new_task)
    next_task_id += 1

    return new_task


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    """UPDATE: полностью обновляет название и статус задачи."""

    task = find_task(task_id)
    title = data.title.strip()

    if not title:
        raise HTTPException(status_code=400, detail="Название не может быть пустым")

    task["title"] = title
    task["is_complete"] = data.is_complete

    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """DELETE: удаляет задачу."""

    task = find_task(task_id)
    tasks.remove(task)

    return Response(status_code=204)
