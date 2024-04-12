from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, RadioField
from wtforms.validators import DataRequired


class InvestorRegisterForm(FlaskForm):
    email = EmailField('1. Логин / email', validators=[DataRequired()])
    password = PasswordField('2. Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('3. Как вас зовут?')
    personal = StringField(
        '5. Расскажите о себе: Какие индустрии рассматриваете для инвестиций, опыт в инвестициях и т.п.')
    capital = IntegerField('6. Сколько вы готовы вложить за год? (в ₽)')
    private_or_fund = RadioField('4. Кем вы являетесь?',
                                 choices=[('fund', 'Венчурный фонд'), ('private', 'Частный инвестор')])
    image = FileField('Загрузите фото профиля')

    submit = SubmitField('Зарегистрироваться')


class BusinessmanRegisterForm(FlaskForm):
    email = EmailField('Логин / email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Как вас зовут?')
    image = FileField('Загрузите фото профиля')

    submit = SubmitField('Зарегистрироваться')
