from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from data.product import Product
from data.users import User
from .parser_order import parser
from data import db_session
from data.order import Order


class OrdersResource(Resource):
    def get(self, orders_id):
        session = db_session.create_session()
        order = session.get(Order, orders_id)
        if not order:
            raise NotFound('Заказ не найден')
        dict_answer = {'orders': order.to_dict(only=('id', 'id_user', 'status', 'price', 'create_date'))}
        products = session.get(Product, order.id_product)
        user = session.get(User, order.id_user)
        if not products:
            dict_answer['orders']['product'] = {}
        else:
            dict_answer['orders']['product'] = products.to_dict()
        if not user:
            dict_answer['orders']['user'] = {}
        else:
            dict_answer['orders']['user'] = user.to_dict(only=('id', 'name', 'surname', 'email', 'phone', 'sex'))

        return jsonify(dict_answer)

    def delete(self, orders_id):
        session = db_session.create_session()
        orders = session.get(Order, orders_id)
        if not orders:
            raise NotFound('Не найден заказ для удаления')
        session.delete(orders)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, orders_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        order = db_sess.get(Order, orders_id)
        if not order:
            raise NotFound('Не найден заказ для изменения')

        elif all(key in args for key in
                 ['id_product', 'id_user', 'status', 'price', 'create_date']):
            for key, value in args.items():
                if key == 'create_date':
                    setattr(order, key, datetime.strptime(value, '%Y-%m-%d %H:%M'))
                else:
                    setattr(order, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class OrdersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        # args = parser.parse_args()
        filters = []
        if 'id_user' in request.args.keys():
            filters.append(Order.id_user == int(request.args['id_user']))
        orders = session.query(Order).filter(*filters)

        dict_resp = {'orders': []}
        for order in orders:
            dict_resp['orders'].append(order.to_dict(only=('id', 'id_user', 'status', 'price')))
            date_create = order.create_date
            if date_create is None:
                dict_resp['orders'][-1]['create_date'] = date_create
            else:
                dict_resp['orders'][-1]['create_date'] = date_create.strftime('%Y-%m-%d')
            products = session.get(Product, order.id_product)
            if not products:
                dict_resp['orders'][-1]['product'] = {}
            else:
                dict_resp['orders'][-1]['product'] = products.to_dict()
        return jsonify(dict_resp)

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in
                 ['id_product', 'id_user', 'status', 'price', 'create_date']):
            db_sess = db_session.create_session()
            orders = Order(
                id_product=args['id_product'],
                id_user=args['id_user'],
                status=args['status'],
                price=args['price'],
                create_date=datetime.strptime(args['create_date'], '%Y-%m-%d %H:%M')
            )
            db_sess.add(orders)
            db_sess.commit()
            return jsonify({'id': orders.id})

        raise BadRequest('Bad Request')
