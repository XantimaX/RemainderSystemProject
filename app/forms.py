from wtforms import FileField, SubmitField,StringField, validators, Field
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,EqualTo,Email


class Upload(FlaskForm):
    file_upload = FileField("Handout Upload" ,validators = [DataRequired(), validators.regexp(u'.*\.(pdf)|(docx)')])
    submit_button = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    password_repeat = StringField("Repeat Password", validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Submit")