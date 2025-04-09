from flask import Flask
from data.db_session import global_init

app = Flask(__name__)

if __name__ == '__main__':
    ses = global_init('db/dynasty.sqlite')
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')
