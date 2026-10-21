from dataclasses import dataclass
import sqlite3


@dataclass
class DbTask:
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


def insert_task(task: DbTask):
    with get_connection() as connection:
        connection.execute(
            """
                INSERT INTO tasks (title, is_complete)
                VALUES (?, ?)
            """,
            (task.title, task.is_complete),
        )


def get_all_tasks() -> list[DbTask]:
    with get_connection() as connection:
        tasks = connection.execute("SELECT * FROM tasks").fetchall()

    return [DbTask(**dict(task)) for task in tasks]


def delete_task(id: int):
    with get_connection() as connection:
        connection.execute("DELETE FROM tasks WHERE id = ?", (id,))


def update_task(id: int, task: DbTask):
    with get_connection() as connection:
        connection.execute(
            """
                UPDATE tasks
                SET title = ?, is_complete = ?
                WHERE id = ?
            """,
            (task.title, task.is_complete, id),
        )
