from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    name = StringField("Activity", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    is_done = BooleanField("Finished")
    submit = SubmitField()


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()