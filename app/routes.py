from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from . import db
from .models import Note, Task
from .forms import NoteForm, TaskForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def dashboard():
    q = request.args.get("q","").strip()
    notes_query = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc())
    tasks_query = Task.query.filter_by(user_id=current_user.id).order_by(Task.done.asc(), Task.due_date.asc().nulls_last())

    if q:
        like = f"%{q}%"
        notes_query = notes_query.filter(or_(Note.title.ilike(like), Note.content.ilike(like)))
        tasks_query = tasks_query.filter(or_(Task.title.ilike(like), Task.description.ilike(like)))

    notes = notes_query.limit(10).all()
    tasks = tasks_query.limit(10).all()
    return render_template("index.html", notes=notes, tasks=tasks, q=q)

# ----- Notes -----
@main_bp.route("/notes")
@login_required
def notes():
    q = request.args.get("q","").strip()
    query = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc())
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Note.title.ilike(like), Note.content.ilike(like)))
    notes = query.all()
    return render_template("notes.html", notes=notes, q=q)

@main_bp.route("/notes/new", methods=["GET","POST"])
@login_required
def note_new():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data or "Untitled", content=form.content.data or "", user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash("Note created.", "success")
        return redirect(url_for("main.notes"))
    return render_template("notes.html", form=form, create=True, notes=[])

@main_bp.route("/notes/<int:note_id>/edit", methods=["GET","POST"])
@login_required
def note_edit(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data or "Untitled"
        note.content = form.content.data or ""
        db.session.commit()
        flash("Note updated.", "success")
        return redirect(url_for("main.notes"))
    return render_template("notes.html", form=form, edit=True, note=note, notes=[])

@main_bp.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def note_delete(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("main.notes"))

# ----- Tasks -----
@main_bp.route("/tasks")
@login_required
def tasks():
    q = request.args.get("q","").strip()
    filter_tab = request.args.get("filter","all")
    query = Task.query.filter_by(user_id=current_user.id)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Task.title.ilike(like), Task.description.ilike(like)))
    if filter_tab == "today":
        query = query.filter(Task.due_date == date.today())
    elif filter_tab == "upcoming":
        query = query.filter(Task.due_date > date.today(), Task.done == False)
    elif filter_tab == "completed":
        query = query.filter(Task.done == True)
    tasks = query.order_by(Task.done.asc(), Task.due_date.asc().nulls_last()).all()
    return render_template("tasks.html", tasks=tasks, q=q, filter_tab=filter_tab)

@main_bp.route("/tasks/new", methods=["GET","POST"])
@login_required
def task_new():
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
        flash("Task created.", "success")
        return redirect(url_for("main.tasks"))
    return render_template("tasks.html", form=form, create=True, tasks=[])

@main_bp.route("/tasks/<int:task_id>/edit", methods=["GET","POST"])
@login_required
def task_edit(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("main.tasks"))
    return render_template("tasks.html", form=form, edit=True, task=task, tasks=[])

@main_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def task_delete(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("main.tasks"))

@main_bp.route("/tasks/<int:task_id>/toggle", methods=["POST"])
@login_required
def task_toggle(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.done = not task.done
    db.session.commit()
    flash("Task updated.", "success")
    return redirect(request.referrer or url_for("main.tasks"))
