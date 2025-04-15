from flask import jsonify
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from .parser_product import parser
from data import db_session
from data.product import Product


class ProductsResource(Resource):
    def get(self, products_id):
        session = db_session.create_session()
        products = session.get(Product, products_id)
        if not products:
            raise NotFound('Заказ не найден')
        return jsonify({'products': products.to_dict(
            only=('id', 'price', 'discount', 'title', 'path_images'))})

    def delete(self, products_id):
        session = db_session.create_session()
        products = session.get(Product, products_id)
        if not products:
            raise NotFound('Не найден товар для удаления')
        session.delete(products)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, products_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        product = db_sess.get(Product, products_id)
        if not product:
            raise NotFound('Не найден товар для изменения')

        elif all(key in args for key in ['price', 'discount', 'title', 'path_images']):
            for key, value in args.items():
                setattr(product, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        products = session.query(Product).all()
        return jsonify({'products': [item.to_dict(
            only=('id', 'price', 'discount', 'title', 'path_images')) for item in products]})

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['price', 'discount', 'title', 'path_images']):
            db_sess = db_session.create_session()
            products = Product(
                title=args['title'],
                discount=args['discount'],
                price=args['price'],
                path_images=args['path_images']
            )
            db_sess.add(products)
            db_sess.commit()
            return jsonify({'id': products.id})

        raise BadRequest('Bad Request')
