from dataclasses import dataclass
import sqlite3


@dataclass
class Task:
    id: int
    title: str
    is_complete: int


def get_connection():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    with get_connection() as connection:
        connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    is_complete INTEGER NOT NULL
                )
                """)


def insert_task(task: Task):
    with get_connection() as connection:
        connection.execute(
            """
                INSERT INTO tasks (title, is_complete)
                VALUES (?, ?)
            """,
            (task.title, task.is_complete),
        )


def get_all_tasks() -> list[Task]:
    with get_connection() as connection:
        tasks = connection.execute("SELECT * FROM tasks").fetchall()

    return [Task(**dict(task)) for task in tasks]


create_table()
insert_task(Task(0, "Задача 1", 1))

tasks = get_all_tasks()
print(tasks)
