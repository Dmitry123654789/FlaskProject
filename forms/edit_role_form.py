from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ChangeRoleForm(FlaskForm):
    user_id = IntegerField('Пользователь', validators=(DataRequired(),))
    role_id = SelectField('Роль', validators=(DataRequired(),),
                          choices=[(1, 'Пользователь'), (2, 'Поддержка'), (3, 'Админ'), (4, 'Глав-админ')])
    submit = SubmitField("Изменить роль")
