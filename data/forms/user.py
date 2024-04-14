from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, RadioField
from wtforms.validators import DataRequired


class InvestorRegisterForm(FlaskForm):
    email = EmailField('1. Логин / email', validators=[DataRequired()])
    password = PasswordField('2. Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('3. Как вас зовут?', validators=[DataRequired()])
    personal = StringField(
        '6. Расскажите о себе: Какие индустрии рассматриваете для инвестиций, опыт в инвестициях и т.п.', validators=[DataRequired()])
    capital = IntegerField('7. Сколько вы готовы вложить за год? (в ₽)', validators=[DataRequired()])
    private_or_fund = RadioField('5. Кем вы являетесь?',
                                 choices=[('fund', 'Венчурный фонд'), ('private', 'Частный инвестор')], validators=[DataRequired()])
    image = FileField('4. Загрузите фото профиля')

    submit = SubmitField('Зарегистрироваться')


class BusinessmanRegisterForm(FlaskForm):
    email = EmailField('Логин / email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Как вас зовут?', validators=[DataRequired()])
    image = FileField('Загрузите фото профиля')

    submit = SubmitField('Зарегистрироваться')
