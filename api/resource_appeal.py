from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from .parser_appeal import parser
from data import db_session
from data.appeal import Appeal


class AppealsResource(Resource):
    def get(self, appeals_id):
        session = db_session.create_session()
        appeals = session.get(Appeal, appeals_id)
        if not appeals:
            raise NotFound('Обращение не найден')
        return jsonify({'appeals': appeals.to_dict(
            only=('id', 'theme', 'question', 'id_user'))})

    def delete(self, appeals_id):
        session = db_session.create_session()
        appeals = session.get(Appeal, appeals_id)
        if not appeals:
            raise NotFound('Не найдено обращение для удаления')
        session.delete(appeals)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, appeals_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        appeal = db_sess.get(Appeal, appeals_id)
        if not appeal:
            raise NotFound('Не найден товар для изменения')

        elif all(key in args for key in ['theme', 'question', 'id_user']):
            for key, value in args.items():
                setattr(appeal, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class AppealsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        filters = []
        if 'id_user' in request.args.keys():
            filters.append(Appeal.id_user == int(request.args['id_user']))
        appeals = session.query(Appeal).filter(*filters)
        return jsonify({'appeals': [item.to_dict(
            only=('id', 'theme', 'question', 'id_user')) for item in appeals]})

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['theme', 'question', 'id_user']):
            db_sess = db_session.create_session()
            appeals = Appeal(
                theme=args['theme'],
                question=args['question'],
                id_user=args['id_user'],
            )
            db_sess.add(appeals)
            db_sess.commit()
            return jsonify({'id': appeals.id})

        raise BadRequest('Bad Request')
