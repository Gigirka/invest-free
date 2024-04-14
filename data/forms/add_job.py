from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    project_name = StringField('Название компании / стартапа', validators=[DataRequired()])
    work_size = StringField('Количество работников', validators=[DataRequired()])
    info = StringField('Расскажите о своей идее как можно подробнее, чтобы привлечь инвесторов', validators=[DataRequired()])
    needed_money = IntegerField('Необходимая сумма инвестиций (в рублях)', validators=[DataRequired()])
    image = FileField('Загрузите превью вашего проекта. Оно сильно повлияет на впечатление инвесторов')

    submit = SubmitField('Опубликовать')