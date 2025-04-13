from datetime import datetime

from flask import jsonify
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from .parser_order import parser
from data import db_session
from data.order import Order


class OrdersResource(Resource):
    def get(self, orders_id):
        session = db_session.create_session()
        orders = session.get(Order, orders_id)
        if not orders:
            raise NotFound('Заказ не найден')
        return jsonify({'orders': orders.to_dict(
            only=('id', 'id_product', 'id_user', 'status', 'price', 'create_date'))})

    def delete(self, orders_id):
        session = db_session.create_session()
        orders = session.get(Order, orders_id)
        if not orders:
            raise NotFound('Не найден заказ ддля удаления')
        session.delete(orders)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, orders_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        order = db_sess.get(Order, orders_id)
        if not order:
            raise NotFound('Не найден заказ ддля изменения')

        elif all(key in args for key in
                 ['id_product', 'id_user', 'status', 'price', 'create_date']) and len(args) == 5:
            for key, value in args.items():
                if key == 'create_date':
                    setattr(order, key, datetime.strptime(value, '%Y-%m-%d %H:%M:%S'))
                else:
                    setattr(order, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class OrdersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        orders = session.query(Order).all()
        return jsonify({'orders': [item.to_dict(
            only=('id', 'id_product', 'id_user', 'status', 'price', 'create_date')) for item in orders]})

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in
                 ['id_product', 'id_user', 'status', 'price', 'create_date']) and len(args) == 5:
            db_sess = db_session.create_session()
            orders = Order(
                id_product=args['id_product'],
                id_user=args['id_user'],
                status=args['status'],
                price=args['price'],
                create_date=datetime.strptime(args['create_date'], '%Y-%m-%d %H:%M:%S')
            )
            db_sess.add(orders)
            db_sess.commit()
            return jsonify({'id': orders.id})

        raise BadRequest('Bad Request')
