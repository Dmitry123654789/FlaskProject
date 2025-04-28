import os
from datetime import datetime
from random import shuffle

from flask import Flask, render_template, request, redirect
from flask import jsonify
from flask import url_for
from flask_login import current_user
from flask_login import logout_user, login_user, LoginManager, login_required
from flask_restful import Api
from requests import get, put
from requests import post
from werkzeug.exceptions import HTTPException

from api import resource_users
from api.resource_appeal import AppealsListResource, AppealsResource
from api.resource_description_product import DescriptionProductsListResource, DescriptionProductsResource
from api.resource_login import LoginResource
from api.resource_order import OrdersListResource, OrdersResource
from api.resource_product import ProductsListResource, ProductsResource
from api.resource_notification import NotificationsListResource, NotificationsResource
from data.admins import check_if_admin
from data.db_session import global_init, create_session
from data.users import User
from forms.add_appeal import AddAppealForm
from forms.user_form import UserForm

my_dir = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
# csrf = CSRFProtect(app)

# api пользователей
api = Api(app)
api.add_resource(resource_users.UserListResource, '/api/users')
api.add_resource(resource_users.UserResource, '/api/users/<int:user_id>')
api.add_resource(LoginResource, '/api/login')

# api заказов
api.add_resource(OrdersListResource, '/api/orders')
api.add_resource(OrdersResource, '/api/orders/<int:orders_id>')

# api товаров
api.add_resource(ProductsListResource, '/api/products')
api.add_resource(ProductsResource, '/api/products/<int:products_id>')

# api описания товаров
api.add_resource(DescriptionProductsListResource, '/api/descriptionproducts')
api.add_resource(DescriptionProductsResource, '/api/descriptionproducts/<int:description_products_id>')

# api обращений пользователей
api = Api(app)
api.add_resource(AppealsListResource, '/api/appeal')
api.add_resource(AppealsResource, '/api/appeal/<int:appeal_id>')

# api уведомление пользователей
api = Api(app)
api.add_resource(NotificationsListResource, '/api/notification')
api.add_resource(NotificationsResource, '/api/notification/<int:appeal_id>')


@login_manager.user_loader
def load_user(user_id):
    sess = create_session()
    user = sess.get(User, user_id)
    user.birth_date = str(user.birth_date).split(' ')[0]
    return user


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


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    """Обрабатывает HTTP-исключения: возвращает JSON или HTML"""

    accept = request.accept_mimetypes
    # Если клиент явно просит JSON или не указал предпочтения
    if accept.accept_json and not accept.accept_html or \
            accept.accept_json and accept.accept_html and accept['application/json'] >= accept['text/html']:
        response = jsonify({
            'error': error.description,
            'status_code': error.code
        })
        response.status_code = error.code
        return response
    else:
        return render_template('fail.html', errr_code=error.code, message=error.description)


@app.errorhandler(Exception)
def handle_generic_exception(error):
    """Обрабатывает все остальные исключения (базовые Exception)"""

    accept = request.accept_mimetypes
    if accept.accept_json and not accept.accept_html or \
            accept.accept_json and accept.accept_html and accept['application/json'] >= accept['text/html']:
        response = jsonify({
            'error': 'Internal Server Error',
            'message': str(error)
        })
        response.status_code = 500
        return response
    else:
        return render_template('fail.html', errr_code=500, message=str(error))


@app.route('/catalog')
def catalog():
    products = get('http://localhost:8080/api/products').json()
    return render_template('catalog.html', products=products)


@app.route('/catalog/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    prod = get(f'http://localhost:8080/api/products/{product_id}').json()['products']
    descript = get(f'http://localhost:8080/api/descriptionproducts/{prod["id_description"]}').json()[
        'description_products']
    products = get('http://localhost:8080/api/products').json()
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('/login')

        json_order = {'id_product': product_id, 'id_user': current_user.id, 'status': 'accepted',
                      'price': prod['price'], 'create_date': datetime.now().strftime('%Y-%m-%d %H:%M')}
        response_order = post('http://localhost:8080/api/orders', json=json_order).json()

        # Добавить уведомление о добавленом заказе

    return render_template('product.html', prod=prod, descript=descript, products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST':
        print(form.validate(), form.errors)
        if form.validate():
            try_post = post('http://localhost:8080/api/users',
                            json={'email': form.email.data, 'password': form.password.data,
                                  'surname': form.surname.data,
                                  'name': form.name.data})
            if try_post.status_code == 400:
                form.email.errors = ['Данный email уже используется']
                return render_template('register.html', form=form)
            elif try_post.status_code == 500:
                return redirect(url_for('server_error'))
            login_user(User(**try_post.json()['user']), remember=True)
            return render_template('register.html', form=form, success=True)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        login_post = post(f'http://localhost:8080/api/login',
                          json={'email': form.email.data, 'password': form.password.data})
        if login_post.status_code == 200:
            user = User(**login_post.json()['user'])
            login_user(user, remember=True)
            return redirect('/')
        elif login_post.status_code == 401:
            form.password.errors = ['Неверный пароль']
        elif login_post.status_code == 404:
            form.email.errors = ['Пользователь не найден']
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    print(current_user.id)
    if current_user.id != user_id and not check_if_admin(current_user.id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    # order = {'status': 'done', 'name': 'Шкаф-купе 175x75', 'price': 56500, 'id': 1}
    return render_template('profile.html', user_id=user_id)


@app.route('/profile/<int:user_id>/info', methods=['GET', 'POST'])
@login_required
def user_info(user_id):
    if current_user.id != user_id and not check_if_admin(current_user.id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    form = UserForm()

    if request.method == 'GET':
        if current_user.id != user_id:
            user = get(f'http://localhost:8080/api/users/{user_id}')
            if user.status_code == 200:
                user = user.json()['user']
                form.phone.data = user['phone']
                form.email.data = user['email']
                form.surname.data = user['surname']
                form.name.data = user['name']
                form.patronymic.data = user['patronymic']
                if user['birth_date']:
                    form.birth_date.data = datetime(*map(int, user['birth_date'].split('-')))
                form.sex.data = user['sex']
            elif user.status_code == 404:
                return render_template('fail.html', message='Пользователь не найден')

        else:
            form.phone.data = current_user.phone
            form.email.data = current_user.email
            form.surname.data = current_user.surname
            form.name.data = current_user.name
            form.patronymic.data = current_user.patronymic
            if current_user.birth_date != 'None':
                form.birth_date.data = datetime(*map(int, current_user.birth_date.split('-')))
            form.sex.data = current_user.sex

    if request.method == 'POST':
        user_json = {
            'phone': form.phone.data,
            'email': form.email.data,
            'surname': form.surname.data,
            'name': form.name.data,
            'patronymic': form.patronymic.data,
            'birth_date': str(form.birth_date.data),
            'sex': form.sex.data,
            'address': form.address.data
        }
        post_status = put(f'http://localhost:8080/api/users/{user_id}', json=user_json)
        if post_status.status_code == 200:
            return render_template('profile_info.html', user_id=user_id, form=form, status_text='Успешно!')
    return render_template('profile_info.html', user_id=user_id, form=form)


@app.route('/profile/<int:user_id>/orders')
@login_required
def user_orders(user_id):
    if current_user.id != user_id and not check_if_admin(current_user.id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    # orders = [{'status': 'sent', 'name': 'Шкаф-купе 175x100', 'price': 120000, 'id': 1},
    #           {'status': 'done', 'name': 'Шкаф-купе 50x75', 'price': 43900, 'id': 2},
    #           {'status': 'construction', 'name': 'Шкаф-купе 175x75', 'price': 210000, 'id': 3}]
    return render_template('profile_orders.html', user_id=user_id)


@app.route('/profile/<int:user_id>/notifications')
@login_required
def user_notifications(user_id):
    if current_user.id != user_id and not check_if_admin(current_user.id):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    # notifications = [
    #     {
    #         'title': 'Новая акция!',
    #         'text': '''Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada.
    #
    #             Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada.''',
    #         'date_short': '29 мар',
    #         'date_full': '29 марта 2025',
    #         'read': True
    #     },
    #     {
    #         'title': 'Новая акция!',
    #         'text': '''Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada. Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada.''',
    #         'date_short': '29 мар',
    #         'date_full': '29 марта 2025',
    #         'read': False
    #     },
    # ]
    return render_template('profile_notifications.html', user_id=user_id)


@app.route('/order/<int:order_id>')
def order(order_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр этого заказа')
    return render_template('order_page.html', order_id=order_id)


if __name__ == '__main__':
    global_init('db/dynasty.sqlite')
    app.run(port=8080, host='127.0.0.1')
