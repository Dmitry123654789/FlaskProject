from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from .parser_notification import parser
from data import db_session
from data.notification import Notification


class NotificationsResource(Resource):
    def get(self, notifications_id):
        session = db_session.create_session()
        notifications = session.get(Notification, notifications_id)
        if not notifications:
            raise NotFound('Уведомление не найдено')
        return jsonify({'notifications': notifications.to_dict(
            only=('id', 'title', 'text', 'public', 'id_user'))})

    def delete(self, notifications_id):
        session = db_session.create_session()
        notifications = session.get(Notification, notifications_id)
        if not notifications:
            raise NotFound('Не найдено уведомление для удаления')
        session.delete(notifications)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, notifications_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        notification = db_sess.get(Notification, notifications_id)
        if not notification:
            raise NotFound('Не найдено уведомление для изменения')

        elif all(key in args for key in ['title', 'text', 'public', 'id_user']):
            for key, value in args.items():
                setattr(notification, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class NotificationsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        filters = []
        if 'id_user' in request.args.keys():
            filters.append(Notification.id_user == request.args.get('id_user'))
        if 'public' in request.args.keys():
            filters.append(Notification.public == request.args.get('public'))
        notifications = session.query(Notification).filter(*filters)
        return jsonify({'notifications': [item.to_dict(
            only=('id', 'title', 'text', 'public', 'id_user')) for item in notifications]})

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['title', 'text', 'public', 'id_user']):
            db_sess = db_session.create_session()
            notifications = Notification(
                title=args['title'],
                text=args['text'],
                public=args['public'],
                id_user=args['id_user']
            )
            db_sess.add(notifications)
            db_sess.commit()
            return jsonify({'id': notifications.id})

        raise BadRequest('Bad Request')