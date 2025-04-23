import os
from random import shuffle

from flask import Flask, render_template, request, redirect
from flask_restful import Api
from requests import post
from flask_login import current_user
from data.db_session import global_init
from forms.add_appeal import AddAppealForm
from api.resource_appeal import AppealsListResource, AppealsResource

app = Flask(__name__)
my_dir = os.path.dirname(__file__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# api обращений пользователей
api = Api(app)
api.add_resource(AppealsListResource, '/api/appeal')
api.add_resource(AppealsResource, '/api/appeal/<int:appeal_id>')

@app.route('/', methods=['GET', 'POST'])
def home_page():
    form = AddAppealForm()
    if form.validate_on_submit():
        appeal_data = {
            'id_user': current_user.id,
            'question': form.question.data,
            'theme': form.theme.data
        }
        post(f'http://localhost:8080/api/appeal', json=appeal_data).json()
        return redirect('/profile')
    return render_template('home.html', form=form)

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
    global_init('db/dynasty.sqlite')
    app.run(port=8080, host='127.0.0.1')
