import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    phone = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String)
    birth_date = sqlalchemy.Column(sqlalchemy.DateTime, default=None)
    sex = sqlalchemy.Column(sqlalchemy.String, default='male')

    admin = orm.relationship('Admin', back_populates='user')
