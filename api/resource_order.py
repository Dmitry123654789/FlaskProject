import datetime

from flask import jsonify, make_response
from flask_restful import Resource, abort
from .parser_order import parser
from data import db_session
from data.order import Order


class OrdersResource(Resource):
    def get(self, orders_id):
        session = db_session.create_session()
        orders = session.get(Order, orders_id)
        if not orders:
            return make_response(jsonify({'error': 'Not found'}), 404)
        return jsonify({'orders': orders.to_dict(
            only=('id', 'id_product', 'id_user', 'status', 'price', 'create_date'))})

    def delete(self, orders_id):
        session = db_session.create_session()
        orders = session.get(Order, orders_id)
        if not orders:
            return make_response(jsonify({'error': 'Not found'}), 404)
        session.delete(orders)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, orders_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        order = db_sess.get(Order, orders_id)
        if not order:
            return make_response(jsonify({'error': 'Not found'}), 404)

        elif all(key in args for key in
                 ['id_product', 'id_user', 'status', 'price', 'create_date']) and len(args) == 5:
            for key, value in args.items():
                if key == 'modified_date':
                    setattr(order, key, datetime.datetime.strptime(args['modified_date'], '%Y-%m-%d %H:%M:%S'))
                else:
                    setattr(order, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        return make_response(jsonify({'error': 'Bad request'}), 400)


class OrdersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        orders = session.query(Order).all()
        return jsonify({'orders': [item.to_dict(
            only=('id', 'id_product', 'id_user', 'status', 'price', 'create_date')) for item in orders]})

    def post(self):
        args = parser.parse_args()
        if not args:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif all(key in args for key in
                 ['id_product', 'id_user', 'status', 'price', 'create_date']) and len(args) == 5:
            db_sess = db_session.create_session()
            orders = Order(
                id_product=args['id_product'],
                id_user=args['id_user'],
                status=args['status'],
                price=args['price'],
                create_date=args['create_date']
            )
            db_sess.add(orders)
            db_sess.commit()
            return jsonify({'id': orders.id})

        return make_response(jsonify({'error': 'Bad request'}), 400)
