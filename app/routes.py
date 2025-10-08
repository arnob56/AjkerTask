from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Task
from app.forms import TaskForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data or "",
            due_date=form.due_date.data,
            priority=form.priority.data,
            done=form.done.data or False,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!", "success")
        return redirect(url_for("main.tasks"))

    # Fetch all tasks for current user
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all()
    return render_template("tasks.html", form=form, tasks=user_tasks)


@main_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("main.tasks"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for("main.tasks"))


@main_bp.route("/tasks/<int:task_id>/toggle", methods=["POST"])
@login_required
def task_toggle(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("main.tasks"))

    task.done = not task.done
    db.session.commit()
    flash("Task status updated!", "info")
    return redirect(url_for("main.tasks"))
