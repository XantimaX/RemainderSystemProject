from wtforms import FileField, SubmitField, validators, Field
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class Upload(FlaskForm):
    file_upload = FileField("Handout Upload" ,validators = [DataRequired(), validators.regexp(u'.*\.(pdf)|(docx)')])
    submit_button = SubmitField("Submit")
