from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название стартапа', validators=[DataRequired()])
    owner = IntegerField('owner id', validators=[DataRequired()])
    work_size = StringField('Количество работников', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    image = FileField('Загрузите превью вашего проекта')

    submit = SubmitField('Submit')