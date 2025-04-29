from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import MultipleFileField, StringField, TextAreaField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    price = IntegerField('Цена товара', validators=[DataRequired()])
    discount = IntegerField('Скидка товара', validators=[], default=0)
    description = TextAreaField('Описание товара', validators=[DataRequired()])
    size = StringField('Размер товара XxYxZ', validators=[DataRequired()])
    type = StringField('Тип товара', validators=[DataRequired()])
    material = StringField('Материал товара', validators=[DataRequired()])
    color = SelectField('Цвет товара', validators=[DataRequired()],
                        choices=[('red', 'Красный'), ('green', 'Зеленый'), ('blue', 'Синий')])
    style = StringField('Стиль товара', validators=[DataRequired()])
    features = StringField('Особенности товара', validators=[DataRequired()])

    images = MultipleFileField('Изображения товара', validators=[DataRequired(),
                                                                 FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                                             'Только изображения!')])

    def to_dict(self):
        return {
            'title': self.title.data,
            'price': self.price.data,
            'discount': self.discount.data,
            'description': self.description.data,
            'size': self.size.data,
            'type': self.type.data,
            'material': self.material.data,
            'color': self.color.data,
            'style': self.style.data,
            'features': self.features.data
        }
