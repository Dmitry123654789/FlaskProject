from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, Label
from wtforms.validators import DataRequired


class AnswerAppealForm(FlaskForm):
    title = StringField('Заголовок ответа:', validators=[DataRequired()])
    answer = TextAreaField('Ответ:', validators=[DataRequired()])
    submit = SubmitField('Отправить ответ', name="save_submit")
    delete_submit = SubmitField('Удалить обращение', name="delete_submit")
