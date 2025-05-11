import os

from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from data.description_product import DescriptionProduct
from .api_tools import check_admin_request
from .parser_product import parser
from data import db_session
from data.product import Product


class ProductsResource(Resource):
    def get(self, products_id):
        session = db_session.create_session()
        product = session.get(Product, products_id)
        if not product:
            raise NotFound('Заказ не найден')

        dict_product = {'products': product.to_dict(only=('id', 'price', 'discount', 'title', 'path_images'))}
        try:
            dict_product['products']['path_images'] = ','.join(os.listdir(dict_product['products']['path_images']))
        except FileNotFoundError:
            dict_product['products']['path_images'] = None
        description_product = session.get(DescriptionProduct, product.id_description)
        if not description_product:
            dict_product['products']['description_products'] = {}
        else:
            dict_product['products']['description_products'] = description_product.to_dict()
        return jsonify(dict_product)

    def delete(self, products_id):
        if check_admin_request(request.headers.get('Authorization')):
            session = db_session.create_session()
            products = session.get(Product, products_id)
            if not products:
                raise NotFound('Не найден товар для удаления')
            desc = session.get(DescriptionProduct, products.id_description)
            try:
                for f in os.listdir(products.path_images):
                    os.remove(os.path.join(products.path_images, f))
                os.rmdir(products.path_images)
            except FileNotFoundError:
                pass
            if desc:
                session.delete(desc)
            session.delete(products)
            session.commit()
            return jsonify({'success': 'OK'})

    def put(self, products_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        product = db_sess.get(Product, products_id)
        if not product:
            raise NotFound('Не найден товар для изменения')

        elif all(key in args for key in ['price', 'discount', 'title', 'path_images', 'id_description']):
            for key, value in args.items():
                setattr(product, key, value)
            db_sess.commit()
            return jsonify({'success': 'OK'})

        raise BadRequest('Bad Request')


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        products = session.query(Product).all()
        dict_products = {'products': []}
        for product in products:
            dict_products['products'].append(product.to_dict(only=('id', 'price', 'discount', 'title', 'path_images')))
            try:
                dict_products['products'][-1]['path_images'] = ','.join(
                    os.listdir(dict_products['products'][-1]['path_images']))
            except FileNotFoundError:
                dict_products['products'][-1]['path_images'] = None
            description_product = session.get(DescriptionProduct, product.id_description)
            if not description_product:
                dict_products['products'][-1]['description_products'] = {}
            else:
                dict_products['products'][-1]['description_products'] = description_product.to_dict()
        return jsonify(dict_products)

    def post(self):
        args = parser.parse_args()
        if not args:
            raise BadRequest('Empty request')

        elif all(key in args for key in ['price', 'discount', 'title', 'path_images', 'id_description']):
            db_sess = db_session.create_session()
            products = Product(
                title=args['title'],
                discount=args['discount'],
                price=args['price'],
                path_images=args['path_images'],
                id_description=args['id_description']
            )
            db_sess.add(products)
            db_sess.commit()
            return jsonify({'id': products.id})

        raise BadRequest('Bad Request')
