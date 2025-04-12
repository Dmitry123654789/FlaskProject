import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    discount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)

    def __repr__(self):
        return self.to_dict()
