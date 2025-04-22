from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class AddAppealForm(FlaskForm):
    theme = StringField('Тема вопроса:', validators=[DataRequired()])
    question = StringField('Вопрос:', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Отправить заявку')