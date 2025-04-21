import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase, create_session


class Admin(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'admins'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), unique=True)
    user = orm.relationship('User', back_populates='admin')

def check_if_admin(user_id):
    sess = create_session()
    admin = sess.query(Admin).filter(Admin.user_id == user_id).first()
    return bool(admin)