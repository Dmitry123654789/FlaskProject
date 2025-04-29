
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, EmailField, TelField, RadioField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp, Optional


class UserForm(FlaskForm):
    phone = TelField('Номер телефона', validators=[Optional(), Regexp(r'^\+?[0-9]{10,15}$',
                                                                                 message='Введите корректный номер телефона')], render_kw={"id": "phone"})
    email = EmailField('Ваш e-mail', validators=[DataRequired()], render_kw={"id": "email"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"id": "password"})
    surname = StringField('Фамилия', validators=[DataRequired()], render_kw={"id": "surname"})
    name = StringField('Имя', validators=[DataRequired()], render_kw={"id": "name"})
    patronymic = StringField('Отчество', validators=[], render_kw={"id": "patronymic"})
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[], render_kw={"id": "birth_date"})
    sex = RadioField('Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], default='male', validators=[DataRequired()], render_kw={"id": "sex"})
    address = StringField('Адрес доставки', validators=[], render_kw={"id": "address"})

    submit = SubmitField('Зарегистрироваться')
