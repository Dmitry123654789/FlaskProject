from flask import jsonify, request
from flask_restful import Resource, abort
from werkzeug.exceptions import NotFound, BadRequest

from .api_tools import check_admin_request
from .parser_description_product import parser
from data import db_session
from data.description_product import DescriptionProduct


class DescriptionProductsResource(Resource):
    def get(self, description_products_id):
        with db_session.create_session() as session:
            description_products = session.get(DescriptionProduct, description_products_id)
            if not description_products:
                raise NotFound('Заказ не найден')
            return jsonify({'description_products': description_products.to_dict(
                only=('id', 'description', 'size', 'type', 'material', 'color', 'style', 'features'))})

    def delete(self, description_products_id):
        if check_admin_request(request.headers.get('Authorization')):
            with db_session.create_session() as session:
                description_products = session.get(DescriptionProduct, description_products_id)
                if not description_products:
                    raise NotFound('Не найден товар для удаления')
                session.delete(description_products)
                session.commit()
            return jsonify({'success': 'OK'})
        abort(403)

    def put(self, description_products_id):
        args = parser.parse_args()
        with db_session.create_session() as session:
            description_product = session.get(DescriptionProduct, description_products_id)
            if not description_product:
                raise NotFound('Не найден описание товара для изменения')

            elif all(key in args for key in ['description', 'size', 'type', 'material', 'color', 'style', 'features']):
                for key, value in args.items():
                    setattr(description_product, key, value)
                session.commit()
                return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class DescriptionProductsListResource(Resource):
    def get(self):
        with db_session.create_session() as session:
            description_products = session.query(DescriptionProduct).all()
            return jsonify({'description_products': [item.to_dict(
                only=('id', 'description', 'size', 'type', 'material', 'color', 'style', 'features')) for item in
                description_products]})

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['description', 'size', 'type', 'material', 'color', 'style', 'features']):
            with db_session.create_session() as session:
                description_products = DescriptionProduct(
                    description=args['description'],
                    size=args['size'],
                    type=args['type'],
                    material=args['material'],
                    color=args['color'],
                    style=args['style'],
                    features=args['features']
                )
                session.add(description_products)
                session.commit()
                return jsonify({'id': description_products.id})

        raise BadRequest('Bad Request')
