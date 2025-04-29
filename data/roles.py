import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Role(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    users = orm.relationship("User", back_populates="role")