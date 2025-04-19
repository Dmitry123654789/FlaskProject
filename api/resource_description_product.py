from flask import jsonify
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from .parser_description_product import parser
from data import db_session
from data.description_product import DescriptionProduct


class DescriptionProductsResource(Resource):
    def get(self, description_products_id):
        session = db_session.create_session()
        description_products = session.get(DescriptionProduct, description_products_id)
        if not description_products:
            raise NotFound('Заказ не найден')
        return jsonify({'description_products': description_products.to_dict(
            only=('id', 'description', 'size', 'type', 'material', 'color', 'style', 'features'))})

    def delete(self, description_products_id):
        session = db_session.create_session()
        description_products = session.get(DescriptionProduct, description_products_id)
        if not description_products:
            raise NotFound('Не найден товар для удаления')
        session.delete(description_products)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, description_products_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        description_product = db_sess.get(DescriptionProduct, description_products_id)
        if not description_product:
            raise NotFound('Не найден описание товара для изменения')

        elif all(key in args for key in ['description', 'size', 'type', 'material', 'color', 'style', 'features']):
            for key, value in args.items():
                setattr(description_product, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class DescriptionProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        description_products = session.query(DescriptionProduct).all()
        return jsonify({'description_products': [item.to_dict(
            only=('id', 'description', 'size', 'type', 'material', 'color', 'style', 'features')) for item in
            description_products]})

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['description', 'size', 'type', 'material', 'color', 'style', 'features']):
            db_sess = db_session.create_session()
            description_products = DescriptionProduct(
                description=args['description'],
                size=args['size'],
                type=args['type'],
                material=args['material'],
                color=args['color'],
                style=args['style'],
                features=args['features']
            )
            db_sess.add(description_products)
            db_sess.commit()
            return jsonify({'id': description_products.id})

        raise BadRequest('Bad Request')
