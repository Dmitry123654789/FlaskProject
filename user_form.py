from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, DateField, SubmitField, StringField,IntegerField, EmailField, RadioField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    email = EmailField('Ваш e-mail', validators=[DataRequired(), Email()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    birth_date = DateField('Дата рождения', format='%Y-%m-%d')
    sex = RadioField('Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], default='male')
    address = StringField('Адрес доставки')

    submit = SubmitField('Сохранить')

    def validate_phone_number(self, phone_number):
        pass