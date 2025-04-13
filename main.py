from flask import Flask
from flask_restful import Api

from api.resource_order import OrdersListResource, OrdersResource
from data import db_session

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api.add_resource(OrdersListResource, '/api/orders')
api.add_resource(OrdersResource, '/api/users/<int:orders_id>')


def main():
    db_session.global_init('db/dynasty.db')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
