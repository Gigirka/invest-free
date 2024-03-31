from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    exp = StringField('Опыт инвестирования')
    speciality = StringField('Образование')
    personal = StringField('Расскажите о себе: Какие индустрии рассматриваете для инвестиций, опыт в инвестициях и т.п.')
    capital = IntegerField('Сколько вы готовы вложить за год?')
    qualification = RadioField('Вы являетесь квалифицированным инвестором?', choices=[('да', 'Да'), ('нет', 'Нет')])
    private_or_fund = RadioField('Кем вы являетесь?', choices=[('fund', 'Венчурный фонд'), ('private', 'Частный инвестор')])
    address = StringField('Адрес')
    money = StringField('Money')
    submit = SubmitField('Submit')