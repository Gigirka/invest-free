from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название стартапа', validators=[DataRequired()])
    work_size = StringField('Количество работников', validators=[DataRequired()])
    image = FileField('Загрузите превью вашего проекта')
    submit = SubmitField('Submit')