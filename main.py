import os
from random import shuffle

from flask import Flask, render_template, request

app = Flask(__name__)
my_dir = os.path.dirname(__file__)


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/portfolio')
def portfolio():
    filters = request.args.getlist('filters')
    all_categories = ['kitchen', 'bed', 'living']

    if not filters:
        filters = all_categories

    direct = os.path.join('static', 'img', 'portfolio')
    all_files = [os.path.join(direct, x) for x in os.listdir(direct)]
    shuffle(all_files)

    # Возвращаем всё, но фильтр передаём отдельно
    return render_template('portfolio.html', images=all_files, active_filters=filters)




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
