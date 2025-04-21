from datetime import datetime as ddt, datetime

from flask import request, jsonify, make_response
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from .parser_user import user_parser
from .responses import bad_request_response


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        filters = []
        if 'sex' in request.args.keys():
            if request.args.get('sex') not in ['female', 'male']:
                return bad_request_response('sex')
            filters.append(User.sex == request.args.get('sex'))
        if 'birthday' in request.args.keys() and request.args.get('birthday') == 'true':
            filters.append(User.birth_date == ddt.now())
        if 'email' in request.args.keys():
            user = session.query(User).filter(User.phone == request.args.get('phone')).first()
            if not user:
                abort(404, message=f'Пользователь с email={request.args.get("phone")} не найден.')
            return jsonify({'user': user.to_dict(
                only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email'))})
        try:
            users = session.query(User).filter(*filters)
        except Exception as e:
            return make_response(jsonify({'message': f'Ошибка на стороне БД.'}), 500)
        return jsonify({'users': [item.to_dict(only=('id', 'surname', 'name', 'email')) for item in users]})

    def post(self):
        try:
            args = user_parser.parse_args()
        except Exception:
            return bad_request_response()
        try:
            new_user = User(**args)
            print(args)
            new_user.set_password(new_user.password)
            if args['birth_date']:
                brth = datetime(*map(int, args['birth_date'].split('-')))
                new_user.birth_date = brth
            sess = db_session.create_session()
            if sess.query(User).filter(User.email == args['email']).first():
                return make_response(jsonify({'message': 'Пользователь с таким email уже существует'}), 400)
            sess.add(new_user)
            sess.commit()
        except Exception as e:
            print(e, new_user.password)
            return make_response(jsonify({'message': f'Ошибка на стороне БД.'}), 500)

        return jsonify({'id': new_user.id})


class UserResource(Resource):
    def get(self, user_id):
        try:
            sess = db_session.create_session()
            user = sess.get(User, user_id)
        except Exception:
            return make_response(jsonify({'message': f'Ошибка на стороне БД.'}), 500)

        if not user:
            return abort(404, message=f'Пользователь с id={user_id} не найден')
        if user.birth_date:
            user.birth_date = datetime.strftime(user.birth_date, '%Y-%m-%d')
        return jsonify(
            {'user': user.to_dict(only=('id', 'surname', 'name', 'patronymic', 'phone', 'birth_date', 'sex', 'email'))})

    def put(self, user_id):
        args = user_parser.parse_args()

        sess = db_session.create_session()
        user = sess.get(User, user_id)
        if not user:
            return make_response(jsonify({'message': f'Пользователь с id={user_id} не найден'}))
        user.surname = args['surname']
        user.name = args['name']
        if 'phone' in args:
            user.phone = args['phone']
        if 'patronymic' in args:
            user.patronymic = args['patronymic']
        if 'birth_date' in args:
            brth = datetime(*map(int, args['birth_date'].split('-')))
            user.birth_date = brth

        user.email = args['email']
        if 'sex' in args:
            user.sex = args['sex']
        print(args)
        sess.commit()
        return jsonify({'message': f'Пользователь с id={user_id} изменен.'}, 201)

    def delete(self, user_id):
        sess = db_session.create_session()
        user = sess.get(User, user_id)
        if not user:
            return abort(404, message=f'Пользователь с id={user_id} не найден.')
        sess.delete(user)
        sess.commit()
        return make_response({'message': f'Пользователь с id={user_id} удалён.'}, 200)
