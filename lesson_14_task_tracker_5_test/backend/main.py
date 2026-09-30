"""Backend планировщика задач на FastAPI и SQLite.

Модуль принимает HTTP-запросы frontend, выполняет SQL-запросы к базе tasks.db
и возвращает результаты в формате JSON.
"""

import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# База хранится рядом с main.py. Путь через __file__ работает независимо от
# каталога, из которого была выполнена команда запуска сервера.
DATABASE_PATH = Path(__file__).with_name("tasks.db")


# -----------------------------------------------------------------------------
# Работа с SQLite
# -----------------------------------------------------------------------------

def get_connection():
    """Создаёт и настраивает отдельное соединение с базой данных."""

    connection = sqlite3.connect(DATABASE_PATH)

    # По умолчанию строка SQLite — это кортеж с числовыми индексами. sqlite3.Row
    # позволяет использовать понятные имена: row["id"], row["title"] и т. д.
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Создаёт таблицу tasks при первом запуске приложения."""

    # Контекстный менеджер фиксирует успешные изменения (commit) и завершает
    # работу с соединением после выхода из блока with.
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_complete INTEGER NOT NULL DEFAULT 0
            )
            """
        )


# -----------------------------------------------------------------------------
# Настройка FastAPI
# -----------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Подготавливает базу до начала обработки HTTP-запросов."""

    # Если таблица уже существует, IF NOT EXISTS сохранит находящиеся в ней
    # задачи и ничего не пересоздаст.
    create_tables()

    # После yield приложение начинает принимать запросы. Код после yield мог бы
    # освобождать общие ресурсы при остановке, но здесь это не требуется.
    yield


app = FastAPI(
    title="Task Tracker API",
    description="Учебный REST API для хранения задач в SQLite",
    lifespan=lifespan,
)


# Frontend и backend используют разные порты, а значит, считаются разными
# origin. CORS разрешает странице с порта 5500 обращаться к API на порту 8000.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Схемы входящих JSON-данных
# -----------------------------------------------------------------------------

class TaskCreate(BaseModel):
    """Тело POST-запроса при создании задачи."""

    title: str


class TaskStatusUpdate(BaseModel):
    """Тело PATCH-запроса при изменении состояния checkbox."""

    is_complete: bool


def task_to_dict(task):
    """Преобразует строку SQLite в словарь для JSON-ответа."""

    return {
        "id": task["id"],
        "title": task["title"],
        # SQLite хранит логическое значение как 0 или 1, а frontend ожидает
        # настоящий JSON boolean: false или true.
        "is_complete": bool(task["is_complete"]),
    }


# -----------------------------------------------------------------------------
# REST API
# -----------------------------------------------------------------------------

@app.get("/api/tasks")
def get_tasks():
    """Возвращает все задачи в порядке их создания."""

    with get_connection() as connection:
        tasks = connection.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()

    # FastAPI автоматически сериализует список словарей в JSON.
    return [task_to_dict(task) for task in tasks]


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Создаёт задачу и возвращает её вместе с назначенным базой id."""

    # Убираем пробелы по краям, чтобы строка из одних пробелов не стала задачей.
    title = task.title.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="Название задачи не может быть пустым",
        )

    with get_connection() as connection:
        # Знаки вопроса обозначают параметры SQL-запроса. Такой способ безопаснее
        # подстановки строк и защищает запрос от SQL-инъекций.
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, is_complete)
            VALUES (?, ?)
            """,
            (title, False),
        )

        # AUTOINCREMENT назначает id в SQLite, а lastrowid возвращает номер
        # только что добавленной строки.
        new_task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return task_to_dict(new_task)


@app.patch("/api/tasks/{task_id}")
def change_task_status(task_id: int, task: TaskStatusUpdate):
    """Меняет только статус выполнения задачи с указанным id."""

    # task_id приходит из URL, а is_complete — из JSON. FastAPI и Pydantic
    # проверят их типы до вызова этой функции.
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE tasks
            SET is_complete = ?
            WHERE id = ?
            """,
            (task.is_complete, task_id),
        )

        # rowcount равен нулю, если строки с таким id в таблице нет.
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        updated_task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

    return task_to_dict(updated_task)


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Удаляет задачу или возвращает 404, если id не существует."""

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Задача не найдена")

    # Статус 204 означает успешное выполнение без тела ответа.
    return Response(status_code=204)
