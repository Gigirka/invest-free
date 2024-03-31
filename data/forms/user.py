from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Логин / email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    #####Для инвестора##################################################################################
    name = StringField('Имя и фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    exp = StringField('Опыт инвестирования')
    speciality = StringField('Образование')
    personal = StringField('Расскажите о себе: Какие индустрии рассматриваете для инвестиций, опыт в инвестициях и т.п.')
    capital = IntegerField('Сколько вы готовы вложить за год?')
    qualification = RadioField('Вы являетесь квалифицированным инвестором?', choices=[('да', 'Да'), ('нет', 'Нет')])
    private_or_fund = RadioField('Кем вы являетесь?', choices=[('fund', 'Венчурный фонд'), ('private', 'Частный инвестор')])
    address = StringField('Адрес проживания')
    #####Для предпринимателя#############################################################################
    money = StringField('Ваш капитал')
    company_name = StringField('Как называется ваша компания?')
    staff = IntegerField('Сколько человек работает в вашей компании?')



    submit = SubmitField('Зарегистрироваться')