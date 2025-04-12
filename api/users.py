from datetime import datetime as ddt

from flask import request, jsonify, make_response, session
from flask_restful import Resource, reqparse

from data import db_session
from data.users import User
from .responses import bad_request


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        filters = []
        if 'sex' in request.args.keys():
            if request.args.get('sex') not in ['female', 'male']:
                return bad_request('sex')
            filters.append(User.sex == request.args.get('sex'))
        if 'birthday' in request.args.keys() and request.args.get('birthday') == 'true':
            filters.append(User.birth_date == ddt.now())
        try:
            users = session.query(User).filter(*filters)
        except Exception:
            return make_response(jsonify({'message': f'Ошибка на стороне БД.'}), 500)
        return jsonify({'users': [item.to_dict(only=('id', 'surname', 'name', 'phone')) for item in users]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('surname', type=str, required=True, help="Surname cannot be blank!")
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('phone', type=str, required=True, help="Name cannot be blank!")
        try:
            args = parser.parse_args()
        except Exception:
            return bad_request()
        try:
            new_user = User(phone=args['phone'], surname=args['surname'], name=args['name'])
            sess = db_session.create_session()
            sess.add(new_user)
            sess.commit()
        except Exception:
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
            return make_response(jsonify({'message': f'Пользователь с id={user_id} не найден'}), 404)
        return jsonify({'user': user.to_dict(only=('id', 'surname', 'name', 'phone', 'birth_date', 'sex', 'email'))})

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('surname', type=str, required=True, help="Surname cannot be blank!")
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('phone', type=str, required=True, help="Phone cannot be blank!")
        parser.add_argument('patronymic', type=str)
        parser.add_argument('birth_date', type=str)
        parser.add_argument('sex', type=str)

        args = parser.parse_args()

        sess = db_session.create_session()
        user = sess.get(User, user_id)
        if not user:
            return make_response(jsonify({'message': f'Пользователь с id={user_id} не найден'}), 404)
        user.surname = args['surname']
        user.name = args['name']
        user.phone = args['phone']
        if 'patronymic' in args:
            user.patronymic = args['patronymic']
        if 'birth_date' in args:
            user.birth_date = args['birth_date']
        if 'sex' in args:
            user.sex = args['sex']

        sess.commit()
        return jsonify({'message': f'Пользователь с id={user_id} изменен.'}, 200)
