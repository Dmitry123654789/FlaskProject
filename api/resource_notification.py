from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.sql.operators import or_
from werkzeug.exceptions import NotFound, BadRequest

from .parser_notification import parser
from data.db_session import create_session
from data.notification import Notification


class NotificationsResource(Resource):
    def get(self, notifications_id):
        session = create_session()
        notifications = session.get(Notification, notifications_id)
        if not notifications:
            raise NotFound('Уведомление не найдено')
        return jsonify({'notifications': notifications.to_dict(
            only=('id', 'title', 'text', 'public', 'read', 'create_date', 'id_user'))})

    def delete(self, notifications_id):
        session = create_session()
        notifications = session.get(Notification, notifications_id)
        if not notifications:
            raise NotFound('Не найдено уведомление для удаления')
        session.delete(notifications)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, notifications_id):
        args = parser.parse_args()
        db_sess = create_session()
        notification = db_sess.get(Notification, notifications_id)
        if not notification:
            raise NotFound('Не найдено уведомление для изменения')

        for key, value in args.items():
            if value is None:
                continue
            if key == 'create_date':
                setattr(notification, key, datetime.strptime(value, '%Y-%m-%d %H:%M'))
            else:
                setattr(notification, key, value)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class NotificationsListResource(Resource):
    def get(self):
        session = create_session()
        if 'id_user' in request.args.keys():
            notifications = session.query(Notification).filter(
                (Notification.id_user == request.args['id_user']) | (Notification.public == True))
        else:
            notifications = session.query(Notification).filter(Notification.public == True)
        return jsonify({'notifications': [item.to_dict(
            only=('id', 'title', 'text', 'public', 'read', 'create_date', 'id_user')) for item in notifications]})

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['title', 'text', 'public', 'read', 'id_user', 'create_date']):
            db_sess = create_session()
            notifications = Notification(
                title=args['title'],
                text=args['text'],
                public=args['public'],
                read=args['read'],
                create_date=datetime.strptime(args['create_date'], '%Y-%m-%d %H:%M'),
                id_user=args['id_user']
            )
            db_sess.add(notifications)
            db_sess.commit()
            return jsonify({'id': notifications.id})

        raise BadRequest('Bad Request')
