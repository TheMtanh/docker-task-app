import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "/app/data/tasks.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def connect():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    return db


with connect() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)


@app.get("/")
def index():
    with connect() as db:
        tasks = db.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", tasks=tasks)


@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    if title and len(title) <= 200:
        with connect() as db:
            db.execute(
                "INSERT INTO tasks (title) VALUES (?)", (title,)
            )
    return redirect(url_for("index"))


@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    with connect() as db:
        db.execute(
            "UPDATE tasks SET done = 1 - done WHERE id = ?",
            (task_id,)
        )
    return redirect(url_for("index"))


@app.post("/delete/<int:task_id>")
def delete(task_id):
    with connect() as db:
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))
