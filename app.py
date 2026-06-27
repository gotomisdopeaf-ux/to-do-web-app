from flask import Flask, redirect, render_template, request, url_for

from database import (
    add_task,
    create_table,
    delete_task,
    get_all_tasks,
    mark_done,
    mark_undone,
)

app = Flask(__name__)

create_table()


@app.route("/")
def index():
    tasks = get_all_tasks()
    pending_tasks = [task for task in tasks if task["done"] == 0]
    completed_tasks = [task for task in tasks if task["done"] == 1]
    return render_template(
        "index.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
    )


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        add_task(title)
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    mark_done(task_id)
    return redirect(url_for("index"))


@app.route("/undo/<int:task_id>", methods=["POST"])
def undo(task_id):
    mark_undone(task_id)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
