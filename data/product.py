import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    discount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    path_images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    id_description = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("description_product.id"), nullable=True)
    product = orm.relationship('DescriptionProduct')

    def __repr__(self):
        return self.to_dict()
