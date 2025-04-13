from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from api.resource_order import OrdersListResource, OrdersResource
from api.resource_product import ProductsListResource, ProductsResource
from api.resource_description_product import DescriptionProductsListResource, DescriptionProductsResource
from data import db_session

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# api заказов
api.add_resource(OrdersListResource, '/api/orders')
api.add_resource(OrdersResource, '/api/orders/<int:orders_id>')

# api товаров
api.add_resource(ProductsListResource, '/api/products')
api.add_resource(ProductsResource, '/api/products/<int:products_id>')

# api описания товаров
api.add_resource(DescriptionProductsListResource, '/api/descriptionproducts')
api.add_resource(DescriptionProductsResource, '/api/descriptionproducts/<int:description_products_id>')


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    """Обрабатывает стандартные HTTP-исключения Flask"""
    response = jsonify({
        'error': error.description,
        'status_code': error.code
    })
    response.status_code = error.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(error):
    """Обрабатывает все остальные исключения (базовые Exception)"""
    response = jsonify({
        'error': 'Internal Server Error',
        'message': str(error)
    })
    response.status_code = 500
    return response


def main():
    db_session.global_init('db/dynasty.db')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
