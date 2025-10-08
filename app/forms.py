from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

# Auth
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")

# Notes
class NoteForm(FlaskForm):
    title = StringField("Title", validators=[Length(max=200)])
    content = TextAreaField("Content", validators=[Optional()])
    submit = SubmitField("Save")

# Tasks
class TaskForm(FlaskForm):
    title = StringField("Task", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[Optional()])
    due_date = DateField("Due Date", validators=[Optional()])
    priority = SelectField("Priority", choices=[("low","Low"),("medium","Medium"),("high","High")], default="medium")
    done = BooleanField("Completed")
    submit = SubmitField("Save")
