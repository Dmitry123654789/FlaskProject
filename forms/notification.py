from flask_wtf import FlaskForm
from wtforms import SubmitField


class NotificationForm(FlaskForm):
    read_submit = SubmitField('Прочитать', name="read")
    deleate_submit = SubmitField('Удалить', name="deleate", id=None)
