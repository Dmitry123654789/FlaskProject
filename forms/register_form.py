from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, EmailField, TelField, RadioField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp, Optional, EqualTo


class RegisterForm(FlaskForm):
    email = EmailField('Ваш e-mail', validators=[DataRequired()], render_kw={"id": "email"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"id": "password"})
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"id": "repeat_password"})
    surname = StringField('Фамилия', validators=[DataRequired()], render_kw={"id": "surname"})
    name = StringField('Имя', validators=[DataRequired()], render_kw={"id": "name"})
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[], render_kw={"id": "birth_date"})
    sex = RadioField('Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], default='male', validators=[DataRequired()], render_kw={"id": "sex"})

    submit = SubmitField('Зарегистрироваться')
