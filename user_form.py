
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, EmailField, TelField, RadioField
from wtforms.validators import DataRequired, Email, Regexp, Optional


class UserForm(FlaskForm):
    phone = TelField('Номер телефона', validators=[Optional(), Regexp(r'^\+?[0-9]{10,15}$',
                                                                                 message='Введите корректный номер телефона')])
    email = EmailField('Ваш e-mail', validators=[DataRequired() ,Email()])
    password = StringField('Пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[])
    name = StringField('Имя', validators=[])
    patronymic = StringField('Отчество')
    birth_date = DateField('Дата рождения', format='%Y-%m-%d')
    sex = RadioField('Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], default='male')
    address = StringField('Адрес доставки')

    submit = SubmitField('Сохранить')
