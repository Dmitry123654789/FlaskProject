import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Notification(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'notification'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    public = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    read = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    user = orm.relationship('User')

    def __repr__(self):
        return self.to_dict()