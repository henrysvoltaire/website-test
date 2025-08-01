import json
import os

from flask import Flask, render_template, request, redirect, session
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return [], [], 0
            return data.get("tasks", []), data.get("archive", []), data.get("next_id", 0)
    return [], [], 0

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump({
            "tasks": tasks,
            "archive": archive,
            "next_id": next_id
        }, file, indent=4)


app = Flask(__name__)
app.secret_key = "key"

tasks, archive, next_id = load_data()
history = []


@app.route("/")
def index():
    sorted_tasks = sorted(tasks, key=lambda t: t["done"])
    sorted_archive = sorted(archive, key=lambda t: t["timestamp"], reverse=True)
    
    latest_archived = session.pop("latest_archived", None)
    archive_reset = session.pop("archive_reset", None)
    data_erased = session.pop("data_erased", None)
    
    return render_template(
        "index.html", 
        tasks=sorted_tasks, 
        latest_archived=latest_archived,
        archive=sorted_archive,
        archive_reset=archive_reset,
        history=history,
        data_erased=data_erased
    )


@app.route("/add", methods=["POST"])
def add():
    global next_id
    task_text = request.form.get("task")

    if task_text and task_text.strip():
        task = {"id": next_id, 
                "text": task_text, 
                "done": False,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        tasks.append(task)
        history.append(f"Added task: '{task_text}'")
        next_id += 1
        save_data()
    
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    task_id = request.form.get("task_id")

    if task_id is not None:
        try:
            id = int(task_id)
        except ValueError:
            return redirect("/")
            
        for i, task in enumerate(tasks):
            if task["id"] == id:
                del tasks[i]
                history.append(f"Task deleted: '{task['text']}'")
                save_data()
                break

    return redirect("/")


@app.route("/toggle", methods=["POST"])
def toggle():
    task_id = request.form.get("task_id")

    if task_id is not None:
        try:
            id = int(task_id)
        except ValueError:
            return redirect("/")
        
        for task in tasks:
            if task["id"] == id:
                task["done"] = not task["done"]
                status = "completed" if task["done"] else "marked as incomplete"
                history.append(f"Task: '{task['text']}' {status}")
                save_data()
                break
    
    return redirect("/")


@app.route("/clear", methods=["POST"])
def clear():
    global archive
    to_archive = [task for task in tasks if task["done"]]
    archive.extend(sorted(to_archive, key=lambda t: t["timestamp"], reverse=True))
    tasks[:] = [task for task in tasks if not task["done"]]
    if to_archive:
        session["latest_archived"] = len(to_archive)
    history.append(f"Archived {len(to_archive)} task(s)")
    
    save_data()
    return redirect("/")


@app.route("/reset", methods=["POST"])
def reset():
    archive.clear()
    session["archive_reset"] = True
    history.append("Archive cleared")
    
    save_data()
    return redirect("/")


@app.route("/erase_data", methods=["POST"])
def erase_data():
    global tasks, archive, history, next_id
    tasks.clear()
    archive.clear()
    history.clear()
    next_id = 0
    
    with open(DATA_FILE, "w") as file:
        json.dump({
            "tasks": [],
            "archive": [],
            "next_id": 0
        }, file, indent=4)

    session["data_erased"] = True
    return redirect("/")


if __name__ == "__main__":
    app.run(debug = True)