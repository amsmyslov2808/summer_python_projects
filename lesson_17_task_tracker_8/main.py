from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import db

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


class WebTask(BaseModel):
    id: int
    title: str
    is_complete: bool


@app.get("/api/tasks")
def get_tasks():
    db_tasks = db.get_all_tasks()
    web_tasks = []

    for db_task in db_tasks:
        web_tasks.append(
            WebTask(
                id=db_task.id,
                title=db_task.title,
                is_complete=True if db_task.is_complete == 1 else False,
            )
        )

    return web_tasks


@app.post("/api/tasks")
def create_new_task(task: WebTask):
    db_task = db.DbTask(
        id=task.id,
        title=task.title,
        is_complete=1 if task.is_complete == True else 0,
    )
    db.insert_task(db_task)


@app.put("/api/tasks/{id}")
def update_task(id: int, task: WebTask):
    db_task = db.DbTask(
        id=id,
        title=task.title,
        is_complete=1 if task.is_complete == True else 0,
    )
    db.update_task(id, db_task)


@app.delete("/api/tasks/{id}")
def delete_task(id: int):
    db.delete_task(id)


if __name__ == "__main__":
    db.create_table()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
