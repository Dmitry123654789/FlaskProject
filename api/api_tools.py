import jwt
from flask import abort

from config import SECRET_KEY
from data import db_session
from data.users import User


def check_admin_request(header: str) -> bool:
    if not header or not header.startswith('Bearer '):
        abort(401, "Токен не передан или неверен.")
    token = header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')
        if not user_id:
            abort(401, "Токен должен содержать ID пользователя")
        session = db_session.create_session()
        if user_id not in [admin.id for admin in session.query(User).filter(User.role_id >= 3)]:
            abort(403, 'У вас нет прав на выполнение этого действия')
        else:
            return True
    except jwt.ExpiredSignatureError:

        abort(401, "Время действия токена истекло")
    except jwt.InvalidTokenError:
        abort(401, "Токен не действителен")
