from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class NotificationForm(FlaskForm):
    title = StringField('Заголовок', validators=(DataRequired(),))
    text = TextAreaField('Основной текст', validators=(DataRequired(),))
    public = BooleanField('Публичный')
    id_user = IntegerField('Получатель', validators=(DataRequired(),))

    def to_dict(self):
        return {
            'title': self.title.data,
            'text': self.text.data,
            'public': self.public.data,
            'id_user': self.id_user.data
        }
