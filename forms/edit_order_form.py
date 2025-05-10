from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class EditOrderForm(FlaskForm):
    state = SelectField('Цвет товара', validators=[DataRequired()],
                        choices=[('ready', 'Заказ готов'), ('sent', 'Заказ в пути'), ('done', 'Заказ завершён'),
                                 ('construction', 'Заказ собирается')])
    save_submit = SubmitField('Сохранить', name="save_submit")
    delete_submit = SubmitField('Удалить', name="save_submit")

    def to_dict(self):
        return {
            'color': self.state.data
        }
