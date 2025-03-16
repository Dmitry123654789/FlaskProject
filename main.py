from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')


if __name__ == '__main__':
    # app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')
