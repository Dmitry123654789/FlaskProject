from flask import Flask
from flask_restful import Api

from api import users_api
from data.db_session import global_init

app = Flask(__name__)
api = Api(app)
api.add_resource(users_api.UserListResource, '/api/users')
api.add_resource(users_api.UserResource, '/api/users/<int:user_id>')

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# @app.errorhandler(400)
# def bad_request(_):
#     return make_response(jsonify({'error': 'Bad Request'}), 400)

if __name__ == '__main__':
    ses = global_init('db/dynasty.sqlite')

    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')
