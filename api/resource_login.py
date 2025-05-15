from flask import make_response
from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.exceptions import NotFound, Unauthorized

from .parser_login import login_parser
from data import db_session
from data.users import User


class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        with db_session.create_session() as session:
            user = session.query(User).filter(User.email == args['email']).first()
            if not user:
                raise NotFound("Пользователь с таким email не найден")
            if not user.check_password(args['password']):
                return make_response(jsonify({'message': 'Неверный пароль'}), 401)
            return make_response(jsonify({'message': 'Успешный вход', 'user': user.to_dict(only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email'))}), 200)

