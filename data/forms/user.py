from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Логин / email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя и фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    experience = StringField('Опыт инвестирования', validators=[DataRequired()])
    speciality = StringField('Образование', validators=[DataRequired()])
    personal = StringField('Расскажите о себе: Какие индустрии рассматриваете для инвестиций, опыт в инвестициях и т.п.', validators=[DataRequired()])
    capital = IntegerField('Сколько вы готовы вложить за год?', validators=[DataRequired()])
    qualification = RadioField('Вы являетесь квалифицированным инвестором?', choices=[('да', 'Да'), ('нет', 'Нет')])
    private_or_fund = RadioField('Кем вы являетесь?', choices=[('fund', 'Венчурный фонд'), ('private', 'Частный инвестор')])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')