import os
from datetime import datetime
from random import shuffle

from flask import Flask, jsonify, render_template
from flask import redirect, request, url_for
from flask_login import current_user, logout_user, login_user, LoginManager, login_required
from flask_restful import Api
from requests import get, put, post, delete
from werkzeug.exceptions import HTTPException

from api import resource_users
from api.resource_appeal import AppealsListResource, AppealsResource
from api.resource_description_product import DescriptionProductsListResource, DescriptionProductsResource
from api.resource_full_product import FullProductResource
from api.resource_login import LoginResource
from api.resource_notification import NotificationsListResource, NotificationsResource
from api.resource_order import OrdersListResource, OrdersResource
from api.resource_product import ProductsListResource, ProductsResource
from data.db_session import global_init, create_session
from data.users import User
from forms.add_appeal import AddAppealForm
from forms.product_form import ProductForm
from forms.register_form import RegisterForm
from forms.user_form import UserForm

my_dir = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

# api пользователей
api = Api(app)
api.add_resource(resource_users.UserListResource, '/api/users')
api.add_resource(resource_users.UserResource, '/api/users/<int:user_id>')
api.add_resource(resource_users.RoleResource, '/api/roles')
api.add_resource(LoginResource, '/api/login')

# api заказов
api.add_resource(OrdersListResource, '/api/orders')
api.add_resource(OrdersResource, '/api/orders/<int:orders_id>')

# api товаров
api.add_resource(ProductsListResource, '/api/products')
api.add_resource(ProductsResource, '/api/products/<int:products_id>')
api.add_resource(FullProductResource, '/api/create_full_product')

# api описания товаров
api.add_resource(DescriptionProductsListResource, '/api/descriptionproducts')
api.add_resource(DescriptionProductsResource, '/api/descriptionproducts/<int:description_products_id>')

# api обращений пользователей
api = Api(app)
api.add_resource(AppealsListResource, '/api/appeal')
api.add_resource(AppealsResource, '/api/appeal/<int:appeals_id>')

# api уведомление пользователей
api = Api(app)
api.add_resource(NotificationsListResource, '/api/notification')
api.add_resource(NotificationsResource, '/api/notification/<int:notifications_id>')


@login_manager.user_loader
def load_user(user_id):
    sess = create_session()
    user = sess.get(User, user_id)
    if user:
        user.birth_date = str(user.birth_date).split(' ')[0]
    return user


def check_if_admin(user):
    return user.role_id >= 3


def check_if_support(user):
    return user.role_id >= 2


# Декоратор для проверки, админ ли пользователь
def admin_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role_id <= 2:
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__  # чтобы Flask не ругался
    return wrapper


def support_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role_id == 1:
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__  # чтобы Flask не ругался
    return wrapper


@support_required
@app.route('/admin')
def admin_page():
    return render_template('admin/admin_base.html')


@support_required
@app.route('/admin/users')
def admin_users():
    return render_template('admin/users_page.html')


@support_required
@app.route('/admin/users/<int:user_id>', methods=['GET', 'POST', 'DELETE'])
def admin_user_page(user_id):
    form = UserForm()
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
        if post_status.status_code == 201:
            return render_template('admin/user.html', user_id=user_id, form=form, status_text='Успешно!',
                                   admin_role=current_user.role_id)
    return render_template('admin/user.html', form=form, user_id=user_id, admin_role=current_user.role_id)


@support_required
@app.route('/admin/appeals')
def appeals_page():
    return render_template('admin/appeals_page.html')


@support_required
@app.route('/admin/appeals/<int:appeal_id>')
def admin_appeal_page():
    return render_template('admin/appeals_page.html')


@admin_required
@app.route('/admin/products')
def admin_products():
    return render_template('admin/products_page.html')


@admin_required
@app.route('/admin/products/create', methods=['GET', 'POST'])
def admin_product_create():
    form = ProductForm()
    if request.method == 'POST':
        files = {
            f'file{i}': (form.images.data[i].filename, form.images.data[i].read(), form.images.data[i].content_type) for
            i in range(len(form.images.data))}

        resp = post('http://localhost:8080/api/create_full_product', data=form.to_dict(), files=files)
        if resp.status_code == 200:
            return render_template('admin/product_create.html', form=form, success=True,
                                   product_id=resp.json()[0]['id'])
    return render_template('admin/product_create.html', form=form)


@admin_required
@app.route('/admin/products/<int:product_id>')
def admin_product_page(product_id):
    return render_template('admin/product.html')


@support_required
@app.route('/admin/orders')
def admin_orders():
    return render_template('admin/orders_page.html')


@admin_required
@app.route('/admin/notifications')
def admin_notifications():
    return render_template('admin/notifications_page.html')


@app.route('/', methods=['GET', 'POST'])
def home_page():
    form = AddAppealForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect('/login')
        appeal_data = {
            'id_user': current_user.id,
            'question': form.question.data,
            'theme': form.theme.data
        }
        notif_data = {
            'title': 'Новое обращение',
            'text': f'Тема: {form.theme.data}\nТекст: {form.question.data}',
            'read': False,
            'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'id_user': current_user.id
        }
        post(f'http://localhost:8080/api/appeal', json=appeal_data).json()
        post(f'http://localhost:8080/api/notification', json=notif_data).json()
        return redirect(f'/profile/{current_user.id}')
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
    products = get('http://localhost:8080/api/products').json()
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('/login')

        json_order = {'id_product': product_id, 'id_user': current_user.id, 'status': 'construction',
                      'price': prod['price'], 'create_date': datetime.now().strftime('%Y-%m-%d %H:%M')}
        response_order = post('http://localhost:8080/api/orders', json=json_order).json()

        notif_json = {
            'title': 'Новый заказ',
            'text': f'Сделан заказ на "{prod["title"]}"',
            'read': False,
            'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'id_user': current_user.id
        }

        post_notif = post('http://localhost:8080/api/notification', json=notif_json)
        return redirect(f'/catalog/{product_id}')
    return render_template('product.html', prod=prod, products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
            try_post = post('http://localhost:8080/api/users',
                            json={'email': form.email.data, 'password': form.password.data,
                                  'surname': form.surname.data,
                                  'name': form.name.data, 'sex': form.sex.data,
                                  'birth_date': str(form.birth_date.data)})
            if try_post.status_code == 400:
                form.email.errors = ['Данный email уже используется']
                return render_template('register.html', form=form)
            elif try_post.status_code == 500:
                return redirect(url_for('server_error'))
            login_user(User(**try_post.json()['user']), remember=True)

            notif_json = {
                'title': 'Регистрация',
                'text': 'Ваш аккаунт зарегистрирован.\nДля изменения данных о пользователе перейдите в раздел "Профиль"',
                'read': False,
                'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'id_user': current_user.id
            }

            post_notif = post('http://localhost:8080/api/notification', json=notif_json)

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


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if current_user.id != user_id and not check_if_admin(current_user):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    form = AddAppealForm()
    if form.validate_on_submit():
        appeal_data = {
            'id_user': user_id,
            'question': form.question.data,
            'theme': form.theme.data
        }
        notif_data = {
            'title': 'Новое обращение',
            'text': f'Тема: {form.theme.data}\nТекст: {form.question.data}',
            'read': False,
            'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'id_user': current_user.id
        }
        post(f'http://localhost:8080/api/notification', json=notif_data).json()
        post(f'http://localhost:8080/api/appeal', json=appeal_data).json()
        return redirect(f'/profile/{user_id}')
    orders = get(f'http://localhost:8080/api/orders?id_user={user_id}')
    order = None
    if orders.status_code == 200 and orders.json()['orders']:
        order = max(orders.json()['orders'], key=lambda x: datetime.strptime(x['create_date'], '%Y-%m-%d'))
    return render_template('profile.html', user_id=user_id, form=form, order=order)


@app.route('/profile/<int:user_id>/info', methods=['GET', 'POST'])
@login_required
def user_info(user_id):
    if current_user.id != user_id and not check_if_admin(current_user):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    form = UserForm()

    if request.method == 'POST':
        if 'save_submit' in request.form:
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
            notif_json = {
                'title': 'Данные пользователя',
                'text': 'Данные вашего аккаунта были изменены, если это были не вы, обратитесь в поддержку',
                'read': False,
                'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'id_user': user_id
            }

            post_status = put(f'http://localhost:8080/api/users/{user_id}', json=user_json)
            post_notif = post('http://localhost:8080/api/notification', json=notif_json)
            if post_status.status_code == 200:
                return redirect(f'/profile/{user_id}/info')
        if 'delete_submit' in request.form:
            orders = get(f'http://localhost:8080/api/orders?id_user={user_id}').json()['orders']
            if len(orders) > 0:
                return render_template('fail.html', errr_code=403, message='У вас есть незавершенные заказы, обратиесь в поддержку для отмены заказа или дождитесь их выполнения')
            logout_user()
            del_user = delete(f'http://localhost:8080/api/users/{user_id}')
            del_notif = delete(f'http://localhost:8080/api/notification?id_user={user_id}')
            del_user = delete(f'http://localhost:8080/api/appeal?id_user={user_id}')
            return redirect('/')
    return render_template('profile_info.html', user_id=user_id, form=form)


@app.route('/profile/<int:user_id>/orders')
@login_required
def user_orders(user_id):
    if current_user.id != user_id and not check_if_admin(current_user):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    orders = get(f'http://localhost:8080/api/orders?id_user={user_id}').json()['orders']
    return render_template('profile_orders.html', user_id=user_id, orders=orders)


@app.route('/profile/<int:user_id>/notifications', methods=['GET', 'POST'])
@login_required
def user_notifications(user_id):
    if current_user.id != user_id and not check_if_admin(current_user):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    if request.method == 'POST':
        if 'delete_submit' in request.form:
            id = request.form.get('delete_submit')
            res = delete(f'http://localhost:8080/api/notification/{id}')

        if 'read_submit' in request.form:
            id = request.form.get('read_submit')
            res = put(f'http://localhost:8080/api/notification/{id}', json={'read': True})
        return redirect(f'/profile/{user_id}/notifications')

    notifications = get(f'http://localhost:8080/api/notification?id_user={user_id}').json()
    return render_template('profile_notifications.html', user_id=user_id, notifications=notifications)


if __name__ == '__main__':
    global_init('db/dynasty.sqlite')
    app.run(port=8080, host='127.0.0.1')
