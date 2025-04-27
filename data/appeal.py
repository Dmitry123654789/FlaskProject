import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Appeal(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'appeal'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    user = orm.relationship('User')

    def __repr__(self):
        return self.to_dict()