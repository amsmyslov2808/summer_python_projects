from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = [
    {"id": 1, "title": "Задача 1", "is_complete": True},
    {"id": 2, "title": "Задача 2", "is_complete": True},
]


def get_task_by_id(id):
    for task in tasks:
        if task["id"] == id:
            return task

    return None


@app.get("/api/tasks")
def get_tasks():
    return tasks


@app.delete("/api/tasks/{id}")
def delete_task(id: int):
    find_task = get_task_by_id(id)

    if find_task == None:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks.remove(find_task)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
