from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from data.users import User
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
            only=('id', 'title', 'text', 'read', 'create_date', 'id_user'))})

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
        filters = []
        if 'id_user' in request.args.keys():
            filters.append(Notification.id_user == request.args['id_user'])

        notifications = session.query(Notification).filter(*filters)
        return jsonify({'notifications': [item.to_dict(
            only=('id', 'title', 'text', 'read', 'create_date', 'id_user')) for item in notifications]})

    def delete(self):
        session = create_session()
        if 'id_user' not in request.args.keys():
            raise BadRequest()

        notifications = session.query(Notification).filter(Notification.id_user == request.args['id_user'])
        for notification in notifications:
            session.delete(notification)
        session.commit()
        return jsonify({'success': 'OK'})


    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['title', 'text', 'read', 'id_user', 'create_date']):
            db_sess = create_session()
            if 'public' in request.args.keys() and request.args['public'] == 'true':
                users_id = db_sess.query(User.id).all()
                for id in users_id:
                    notifications = Notification(
                        title=args['title'],
                        text=args['text'],
                        read=args['read'],
                        create_date=datetime.strptime(args['create_date'], '%Y-%m-%d %H:%M'),
                        id_user=id[0]
                    )
                    db_sess.add(notifications)
                db_sess.commit()
                return jsonify({'success': 'OK'})
            else:
                notifications = Notification(
                    title=args['title'],
                    text=args['text'],
                    read=args['read'],
                    create_date=datetime.strptime(args['create_date'], '%Y-%m-%d %H:%M'),
                    id_user=args['id_user']
                )
                db_sess.add(notifications)
                db_sess.commit()
                return jsonify({'id': notifications.id})

        raise BadRequest('Bad Request')