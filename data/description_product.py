import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class DescriptionProduct(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'description_product'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Описание
    size = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Тип (стол, шкаф, кровать и т. д.)
    material = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    style = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Стиль (лофт, классика, модерн и т. д.)
    features = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Особенности (раздвижной, трансформер и т. д.)

    def __repr__(self):
        return self.to_dict()
