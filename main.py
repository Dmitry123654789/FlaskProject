import os
from random import shuffle

from flask import Flask, render_template, request
from flask import Flask, render_template, redirect, request, session, url_for
from flask_login import current_user, user_unauthorized, login_manager
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect
from requests import post
from flask import Flask, jsonify, render_template
from flask_restful import Api
from requests import get
from werkzeug.exceptions import HTTPException
from api.resource_order import OrdersListResource, OrdersResource
from api.resource_product import ProductsListResource, ProductsResource
from api.resource_description_product import DescriptionProductsListResource, DescriptionProductsResource
from data import db_session

from api import users_api
from data.__all_models import *
from data.admins import check_if_admin
from data.db_session import global_init, create_session
from user_form import UserForm

my_dir = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# csrf = CSRFProtect(app)

api = Api(app)
api.add_resource(users_api.UserListResource, '/api/users')
api.add_resource(users_api.UserResource, '/api/users/<int:user_id>')

# api заказов
api.add_resource(OrdersListResource, '/api/orders')
api.add_resource(OrdersResource, '/api/orders/<int:orders_id>')

# api товаров
api.add_resource(ProductsListResource, '/api/products')
api.add_resource(ProductsResource, '/api/products/<int:products_id>')

# api описания товаров
api.add_resource(DescriptionProductsListResource, '/api/descriptionproducts')
api.add_resource(DescriptionProductsResource, '/api/descriptionproducts/<int:description_products_id>')


# @login_manager.user_loader
# def load_user(user_id):
#     sess = create_session()
#     return sess.get(users.User, int(user_id))

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


@app.route('/catalog')
def catalog():
    products = get('http://localhost:8080/api/products').json()
    return render_template('catalog.html', products=products)


@app.route('/catalog/<int:product_id>')
def product(product_id):
    prod = get(f'http://localhost:8080/api/products/{product_id}').json()['products']
    descript = get(f'http://localhost:8080/api/descriptionproducts/{prod["id_description"]}').json()[
        'description_products']
    products = get('http://localhost:8080/api/products').json()
    return render_template('product.html', prod=prod, descript=descript, products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST':
        if form.validate():
            try_post = post('http://localhost:8080/api/users',
                            json={'phone': form.phone_number.data, 'surname': form.surname.data,
                                  'name': form.name.data})
            print(try_post.json())
            if try_post.status_code == 400:
                form.phone_number.errors = ['Данный номер телефона уже используется']
                return render_template('register.html', form=form)
            elif try_post.status_code == 500:
                return redirect(url_for('server_error'))
            return render_template('register.html', form=form, success=True)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        if request.form.get('verif_code', False):
            #  TODO: регистрация пользователя
            if request.form.get('verif_code', False) == session.get('verification_code', '00000'):
                return redirect('/')
            return render_template('login.html', form=form, log_status='waiting_for_code', verif_error='Неверный код')
        else:
            if form.phone_number.validate(form):
                session['verification_code'] = '12345'
                return render_template('login.html', form=form, log_status='waiting_for_code')
    return render_template('login.html', form=form, log_status='password')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    redirect('/')


@app.route('/profile/<int:user_id>')
def profile(user_id):
    if user_unauthorized or current_user.id != user_id and not check_if_admin(user_id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    order = {'status': 'done', 'name': 'Шкаф-купе 175x75', 'price': 56500, 'id': 1}
    return render_template('profile.html', user_id=user_id, order=order)


@app.route('/profile/<int:user_id>/info', methods=['GET', 'POST'])
def user_info(user_id):
    if user_unauthorized or current_user.id != user_id and not check_if_admin(user_id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    form = UserForm()
    sess = create_session()
    user = sess.get(users.User, user_id)

    if request.method == 'GET':
        if not user:
            return render_template('fail.html', message='Пользователя не существует.')

        form.phone_number.data = user.phone_number
        form.email.data = user.email
        form.surname.data = user.surname
        form.name.data = user.name
        form.patronymic.data = user.patronymic
        form.birth_date.data = user.birth_date
        form.sex.data = user.sex
        form.address.data = user.address

    if request.method == 'POST':
        if user:
            user.phone_number = form.phone_number.data
            user.email = form.email.data
            user.surname = form.surname.data
            user.name = form.name.data
            user.patronymic = form.patronymic.data
            user.birth_date = form.birth_date.data
            user.sex = form.sex.data
            user.address = form.address.data
    return render_template('profile_info.html', user_id=user_id, form=form)


@app.route('/profile/<int:user_id>/orders')
def user_orders(user_id):
    if user_unauthorized or current_user.id != user_id and not check_if_admin(user_id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    orders = [{'status': 'sent', 'name': 'Шкаф-купе 175x100', 'price': 120000, 'id': 1},
              {'status': 'done', 'name': 'Шкаф-купе 50x75', 'price': 43900, 'id': 2},
              {'status': 'construction', 'name': 'Шкаф-купе 175x75', 'price': 210000, 'id': 3}]
    return render_template('profile_orders.html', user_id=user_id, orders=orders)


@app.route('/profile/<int:user_id>/notifications')
def user_notifications(user_id):
    if user_unauthorized or current_user.id != user_id and not check_if_admin(user_id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    notifications = [
        {
            'title': 'Новая акция!',
            'text': '''Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. 

                Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada.''',
            'date_short': '29 мар',
            'date_full': '29 марта 2025',
            'read': True
        },
        {
            'title': 'Новая акция!',
            'text': '''Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada.''',
            'date_short': '29 мар',
            'date_full': '29 марта 2025',
            'read': False
        },
    ]
    return render_template('profile_notifications.html', user_id=user_id, notifications=notifications)


@app.route('/order/<int:order_id>')
def order(order_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр этого заказа')
    return render_template('order_page.html', order_id=order_id)


if __name__ == '__main__':
    global_init('db/dynasty.sqlite')
    app.run(port=8080, host='127.0.0.1')
