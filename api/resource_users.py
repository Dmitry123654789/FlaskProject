from datetime import datetime as ddt, datetime

from flask import request, jsonify, make_response, abort
from flask_restful import Resource

from data import db_session
from data.roles import Role
from data.users import User
from .api_tools import check_admin_request, check_user_is_user_request
from .parser_user import user_parser


def check_password(pas: str) -> str:
    if len(pas) < 8:
        return 'Пороль должен быть не менее 8 символов'
    if not any([x.isalpha() for x in pas]):
        return 'Пороль должен содеожать хотя бы одну букву'
    if not any([x.isdigit() for x in pas]):
        return 'Пароль должен содержать хотя бы одну цифру'
    return ''


class UserListResource(Resource):
    def get(self):
        with db_session.create_session() as session:
            filters = []
            if 'sex' in request.args.keys():
                if request.args.get('sex') not in ['female', 'male']:
                    return abort(400, 'Пол должен быть указан как: male или female')
                filters.append(User.sex == request.args.get('sex'))
            if 'birthday' in request.args.keys() and request.args.get('birthday') == 'true':
                filters.append(User.birth_date == ddt.now())
            if 'email' in request.args.keys():
                user = session.query(User).filter(User.email == request.args.get('email')).first()
                if not user:
                    return abort(404, f'Пользователь с email={request.args.get("email")} не найден.')
                return jsonify({'user': user.to_dict(
                    only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email', 'role_id'))})

            users = session.query(User).filter(*filters)
            if 'full' in request.args.keys():
                return jsonify({'users': [item.to_dict(
                    only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email', 'role_id')) for
                    item
                    in
                    users]})
            return jsonify({'users': [item.to_dict(only=('id', 'surname', 'name', 'email')) for item in users]})

    def post(self):
        args = user_parser.parse_args()
        new_user = User(**args)

        new_user.role_id = 1
        new_user.set_password(new_user.password)
        if args['birth_date']:
            brth = datetime(*map(int, args['birth_date'].split('-')))
            new_user.birth_date = brth
        with db_session.create_session() as session:
            if session.query(User).filter(User.email == args['email']).first():
                return abort(403, 'email Пользователь с таким email уже существует')
            if check_password(args['password']):
                return abort(403, f'password {check_password(args['password'])}')
            session.add(new_user)
            session.commit()

            return jsonify({'id': new_user.id, 'user': new_user.to_dict(
                only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email', 'role_id'))})


class UserResource(Resource):
    def get(self, user_id):
        with db_session.create_session() as session:
            user = session.get(User, user_id)
            if not user:
                return abort(404, f'Пользователь с id={user_id} не найден')

            if user.birth_date:
                user.birth_date = datetime.strftime(user.birth_date, '%Y-%m-%d')
            return jsonify(
                {'user': user.to_dict(
                    only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email', 'role_id'))})

    def put(self, user_id):
        args = user_parser.parse_args()
        with db_session.create_session() as session:
            user = session.get(User, user_id)
            if not user:
                return abort(404, f'Пользователь с id={user_id} не найден')
            for key, value in args.items():
                if value is None:
                    continue
                if key == 'birth_date':
                    setattr(user, key, datetime.strptime(value, '%Y-%m-%d'))
                elif key == 'role_id':
                    #  Проверка того, что отправляющий - админ
                    if check_admin_request(request.headers.get('Authorization')):
                        user.role_id = value
                else:
                    setattr(user, key, value)
            session.commit()
            return jsonify({'message': f'Пользователь с id={user_id} изменен.', 'user': user.to_dict(
                only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email', 'role_id'))})

    def delete(self, user_id):
        if check_admin_request(request.headers.get('Authorization')) or \
                check_user_is_user_request(request.headers.get('Authorization'), user_id):
            with db_session.create_session() as session:
                user = session.get(User, user_id)
                if not user:
                    return abort(404, f'Пользователь с id={user_id} не найден')
                session.delete(user)
                session.commit()
            return make_response({'message': f'Пользователь с id={user_id} удалён.'}, 200)


class RoleResource(Resource):
    def get(self):
        with db_session.create_session() as session:
            roles = session.query(Role).all()
            return make_response({'roles': [item.to_dict(only=('id', 'name')) for item in roles]}, 200)
