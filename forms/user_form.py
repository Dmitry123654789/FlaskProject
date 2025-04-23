
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, EmailField, TelField, RadioField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp, Optional


class UserForm(FlaskForm):
    phone = TelField('Номер телефона', validators=[Optional(), Regexp(r'^\+?[0-9]{10,15}$',
                                                                                 message='Введите корректный номер телефона')])
    email = EmailField('Ваш e-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[])
    sex = RadioField('Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], default='male', validators=[DataRequired()])
    address = StringField('Адрес доставки', validators=[])

    submit = SubmitField('Зарегистрироваться')
