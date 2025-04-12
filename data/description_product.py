import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class DescriptionProduct(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'descriptions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    id_product = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"), nullable=True)
    product = orm.relationship('Product')

    def __repr__(self):
        return self.to_dict()
