import os
from datetime import datetime
from random import shuffle

from flask import Flask, render_template, jsonify
from flask import redirect, request, url_for
from flask_login import current_user, logout_user, login_user, LoginManager, login_required
from flask_restful import Api
from requests import get, put, post, delete
from waitress import serve
from werkzeug.exceptions import HTTPException

from api import resource_users
from api.resource_appeal import AppealsListResource, AppealsResource
from api.resource_description_product import DescriptionProductsListResource, DescriptionProductsResource
from api.resource_full_product import FullProductResource
from api.resource_login import LoginResource
from api.resource_notification import NotificationsListResource, NotificationsResource
from api.resource_order import OrdersListResource, OrdersResource
from api.resource_product import ProductsListResource, ProductsResource
from config import SECRET_KEY, generate_token
from data.db_session import global_init, create_session
from data.users import User
from forms.add_appeal import AddAppealForm
from forms.appeal_answer_form import AnswerAppealForm
from forms.edit_order_form import EditOrderForm
from forms.edit_role_form import ChangeRoleForm
from forms.notification_form import NotificationForm
from forms.product_form import ProductForm
from forms.register_form import RegisterForm
from forms.user_form import UserForm

my_dir = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
API_DOMEN = 'dmitry123654789-flaskproject-fe06.twc1.net'

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
api.add_resource(FullProductResource, '/api/full_product')

# api описания товаров
api.add_resource(DescriptionProductsListResource, '/api/descriptionproducts')
api.add_resource(DescriptionProductsResource, '/api/descriptionproducts/<int:description_products_id>')

# api обращений пользователей
api.add_resource(AppealsListResource, '/api/appeal')
api.add_resource(AppealsResource, '/api/appeal/<int:appeals_id>')

# api уведомление пользователей
api.add_resource(NotificationsListResource, '/api/notification')
api.add_resource(NotificationsResource, '/api/notification/<int:notifications_id>')

global_init('db/dynasty.sqlite')


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
            return redirect(url_for('home_page'))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__  # чтобы Flask не ругался
    return wrapper


def support_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role_id == 1:
            return redirect(url_for('home_page'))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__  # чтобы Flask не ругался
    return wrapper


@app.route('/admin/admins', methods=['GET', 'POST'])
@admin_required
def admin_page():
    form = ChangeRoleForm()
    if request.method == 'POST':
        form.validate()
        tokn = generate_token({'id': current_user.id, 'role_id': current_user.role_id})
        change_req = put(f'http://localhost:5000/api/users/{form.user_id.data}', json={'role_id': form.role_id.data},
                         headers={'Authorization': 'Bearer ' + tokn})
        if change_req.status_code == 200:
            form.submit.errors = ['Успешно!']
        elif change_req.status_code == 404:
            form.user_id.errors = ['Пользователь не найден']
        else:
            form.user_id.errors = [change_req.json()]
    return render_template('admin/admins_page.html', form=form)


@app.route('/admin/users')
@support_required
def admin_users():
    return render_template('admin/users_page.html')


@app.route('/admin/users/<int:user_id>', methods=['GET', 'POST'])
@support_required
def admin_user_page(user_id):
    form = UserForm()
    if request.method == 'POST':
        if 'save_submit' in request.form:
            if current_user.role_id < 3:
                return render_template('fail.html', message='У вас нет прав на эти действия')
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

            post_status = put(f'http://localhost:5000/api/users/{user_id}', json=user_json)
            if post_status.status_code == 201:
                return render_template('admin/user.html', user_id=user_id, form=form, status_text='Успешно!',
                                       admin_role=current_user.role_id)

        if 'delete_submit' in request.form:
            if current_user.role_id != 4:
                return render_template('fail.html', message='У вас нет прав на эти действия')
            orders = get(f'http://localhost:5000/api/orders?id_user={user_id}').json()['orders']
            if len(orders) > 0:
                return render_template('fail.html', errr_code=403,
                                       message='У вас есть незавершенные заказы, обратиесь в поддержку для отмены заказа или дождитесь их выполнения')
            tokn = generate_token({'id': current_user.id})
            del_user = delete(f'http://localhost:5000/api/users/{user_id}', headers={'Authorization': 'Bearer ' + tokn})
            del_notif = delete(f'http://localhost:5000/api/notification?id_user={user_id}')
            del_appeal = delete(f'http://localhost:5000/api/appeal?id_user={user_id}')
            if current_user.id == user_id:
                logout_user()
                return redirect('/')
            return redirect('/admin/users')
    return render_template('admin/user.html', form=form, user_id=user_id, admin_role=current_user.role_id)


@app.route('/admin/appeals')
@support_required
def appeals_page():
    return render_template('admin/appeals_page.html')


@app.route('/admin/appeals/<int:appeal_id>', methods=['GET', 'POST'])
@support_required
def admin_send_appeal_answer(appeal_id):
    form = AnswerAppealForm()
    appeal = get(f'http://localhost:5000/api/appeal/{appeal_id}')
    if appeal.status_code == 404:
        return render_template('fail.html', message='Не найден вопрос', errr_code=404)
    form.title.data = 'Ответ на обращение: ' + str(appeal_id)
    if request.method == 'POST':
        if 'save_submit' in request.form:
            answer_notification = {'title': form.title.data,
                                   'text': form.answer.data,
                                   'read': False,
                                   'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                   'id_user': appeal.json()['appeals']['id_user']}
            answer_post = post(f'http://localhost:5000/api/notification', json=answer_notification)
            if answer_post.status_code == 200:
                return render_template('admin/appeal_answer_create.html', form=form, appeal_id=appeal_id,
                                       appeal=appeal.json()['appeals'], status_text='Успешно!')
        if 'delete_submit' in request.form:
            answer_post = delete(f'http://localhost:5000/api/appeal/{appeal_id}')
            if answer_post.status_code == 200:
                return redirect('/admin/appeals')

    return render_template('admin/appeal_answer_create.html', form=form, appeal_id=appeal_id,
                           appeal=appeal.json()['appeals'])


@app.route('/admin/products')
@admin_required
def admin_products():
    return render_template('admin/products_page.html')


@app.route('/admin/products/create', methods=['GET', 'POST'])
@admin_required
def admin_product_create():
    form = ProductForm()
    if request.method == 'POST':
        files = {
            f'file{i}': (form.images.data[i].filename, form.images.data[i].read(), form.images.data[i].content_type) for
            i in range(len(form.images.data))}

        resp = post(f'http://localhost:5000/api/full_product', data=form.to_dict(), files=files)
        if resp.status_code == 200:
            return render_template('admin/product_create.html', form=form, success=True,
                                   product_id=resp.json()[0]['id'])
    return render_template('admin/product_create.html', form=form)


@app.route('/admin/products/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_product_page(product_id):
    form = ProductForm()
    product_req = get(f'http://localhost:5000/api/products/{product_id}')
    if product_req.status_code == 404:
        return render_template('fail.html', message='Продукт не найден', errr_code='404')
    product = product_req.json()['products']
    if request.method == 'POST':
        if 'save_sub' in request.form:
            files = {
                f'file{i}': (form.images.data[i].filename, form.images.data[i].read(), form.images.data[i].content_type)
                for
                i in range(len(form.images.data))}
            resp = put(f'http://localhost:5000/' + 'api/full_product?description_id={}&product_id={}'.format(
                product['description_products']['id'], product_id), data=form.to_dict(), files=files)
            if resp.status_code == 200:
                return redirect(f'/admin/products/{product_id}')
            return render_template('fail.html', message='Произошла ошибка при заполнении данных', errr_code='403')

        if 'delete_submit' in request.form:
            tokn = generate_token({'id': current_user.id})
            resp = delete(f'http://localhost:5000/api/products/{product_id}',
                          headers={'Authorization': 'Bearer ' + tokn})
            if resp.status_code == 200:
                return redirect(f'/admin/products')
            return render_template('fail.html', message='Произошла ошибка', errr_code=500)

    form.title.data = product['title']
    form.price.data = product['price']
    form.discount.data = product['discount']
    form.description.data = product['description_products']['description']
    form.size.data = product['description_products']['size']
    form.type.data = product['description_products']['type']
    form.material.data = product['description_products']['material']
    form.color.data = product['description_products']['color']
    form.style.data = product['description_products']['style']
    form.features.data = product['description_products']['features']
    form.images.data = product['path_images']
    return render_template('admin/product_edit.html', form=form)


@app.route('/admin/orders')
@support_required
def admin_orders():
    return render_template('admin/orders_page.html')


@app.route('/admin/notifications')
@admin_required
def admin_notifications():
    return render_template('admin/notifications_page.html')


@app.route('/admin/notifications/create', methods=['GET', 'POST'])
@admin_required
def admin_notification_create():
    form = NotificationForm()
    if request.method == 'POST':
        notif_json = form.to_dict()
        notif_json.update({'read': False, 'create_date': datetime.now().strftime('%Y-%m-%d %H:%M')})
        if notif_json['public']:
            resp = post(f'http://localhost:5000/api/notification?public=true', json=notif_json)
        else:
            resp = post(f'http://localhost:5000/api/notification', json=notif_json)
        if resp.status_code == 200:
            return render_template('admin/notification_create.html', form=form, success=True)

    return render_template('admin/notification_create.html', form=form)


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
        post(f'http://localhost:5000/api/appeal', json=appeal_data).json()
        post(f'http://localhost:5000/api/notification', json=notif_data).json()
        return redirect(f'/profile/{current_user.id}')
    return render_template('home.html', form=form)


@app.route('/portfolio')
def portfolio():
    direct = os.path.join('static', 'img', 'products')
    all_files1 = [[os.path.join(direct, x, i) for i in os.listdir(os.path.join(direct, x))] for x in os.listdir(direct)
                  if x != 'no_prod.png']
    all_files = []
    for file in all_files1:
        all_files.extend(file)
    shuffle(all_files)

    return render_template('portfolio.html', images=all_files)


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
    products = get(f'http://localhost:5000/api/products').json()
    return render_template('catalog.html', products=products)


@app.route('/catalog/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    prod = get(f'http://localhost:5000/api/products/{product_id}').json()['products']
    products = get(f'http://localhost:5000/api/products').json()
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('/login')

        json_order = {'id_product': product_id, 'id_user': current_user.id, 'status': 'construction',
                      'price': prod['price'], 'create_date': datetime.now().strftime('%Y-%m-%d %H:%M')}
        response_order = post(f'http://localhost:5000/api/orders', json=json_order).json()

        notification = {'title': 'Регистрация заказа №' + str(response_order['id']),
                        'text': f'\tЗдравствуйте, {current_user.name}! Ваш заказ товара "{prod["title"]}" был оформел, и в скорем времени мы приступим к его выполнению.\n\n\tСпасибо, что выбираете нас!',
                        'public': False, 'read': False, 'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'id_user': current_user.id}
        post(f'http://localhost:5000/api/notification', json=notification)
    return render_template('product.html', prod=prod, products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
            try_post = post(f'http://localhost:5000/api/users',
                            json={'email': form.email.data, 'password': form.password.data,
                                  'surname': form.surname.data,
                                  'name': form.name.data, 'sex': form.sex.data,
                                  'birth_date': str(form.birth_date.data)})
            print(try_post.json())
            if try_post.status_code == 403:
                field, mes = try_post.json()['message'].split(maxsplit=1)
                if field == 'email':
                    form.email.errors = [mes]
                    return render_template('register.html', form=form)
                if field == 'password':
                    form.password.errors = [mes]
                    return render_template('register.html', form=form)
            if try_post.status_code == 500:
                return redirect(url_for('server_error'))
            if try_post.status_code == 400:
                form.password.errors = [try_post.json()['error']]
                return render_template('register.html', form=form)
            login_user(User(**try_post.json()['user']), remember=True)

            notif_json = {
                'title': 'Регистрация',
                'text': 'Ваш аккаунт зарегистрирован.\nДля изменения данных о пользователе перейдите в раздел "Профиль"',
                'read': False,
                'create_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'id_user': current_user.id
            }

            post_notif = post(f'http://localhost:5000/api/notification', json=notif_json)

            return render_template('register.html', form=form, success=True)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        login_post = post(f'http://localhost:5000/api/login',
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
        post(f'http://localhost:5000/api/notification', json=notif_data).json()
        post(f'http://localhost:5000/api/appeal', json=appeal_data).json()
        return redirect(f'/profile/{user_id}')
    orders = get(f'http://localhost:5000/api/orders?id_user={user_id}')
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

            post_status = put(f'http://localhost:5000/api/users/{user_id}', json=user_json)
            post_notif = post(f'http://localhost:5000/api/notification', json=notif_json)
            if post_status.status_code == 200:
                logout_user()
                login_user(User(**post_status.json()['user']), remember=True)
                return redirect(f'/profile/{user_id}/info')
        if 'delete_submit' in request.form:
            orders = get(f'http://localhost:5000/api/orders?id_user={user_id}').json()['orders']
            if len(orders) > 0:
                return render_template('fail.html', errr_code=403,
                                       message='У вас есть незавершенные заказы, обратиесь в поддержку для отмены заказа или дождитесь их выполнения')
            tokn = generate_token({'id': current_user.id})
            del_user = delete(f'http://localhost:5000/api/users/{user_id}', headers={'Authorization': 'Bearer ' + tokn})
            del_notif = delete(f'http://localhost:5000/api/notification?id_user={user_id}')
            del_user = delete(f'http://localhost:5000/api/appeal?id_user={user_id}')
            logout_user()
            return redirect('/')
        form.phone.data = current_user.phone
        form.email.data = current_user.email
        form.surname.data = current_user.surname
        form.name.data = current_user.name
        form.patronymic.data = current_user.patronymic
        form.birth_date.data = datetime.strptime(current_user.birth_date, '%Y-%m-%d')
        form.sex.data = current_user.sex
    return render_template('profile_info.html', user_id=user_id, form=form)


@app.route('/profile/<int:user_id>/orders')
@login_required
def user_orders(user_id):
    if current_user.id != user_id and not check_if_admin(current_user):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    orders = get(f'http://localhost:5000/api/orders?id_user={user_id}').json()['orders']
    return render_template('profile_orders.html', user_id=user_id, orders=orders)


@app.route('/order/<int:order_id>', methods=['POST', "GET"])
@login_required
def order_page(order_id):
    form = EditOrderForm()
    order_req = get(f'http://localhost:5000/api/orders/{order_id}')
    if order_req.status_code == 404:
        return render_template('fail.html', message='Заказ не найден.', errr_code='404')
    order = order_req.json()['orders']
    if request.method == 'POST':
        if 'save_submit' in request.form and check_if_admin(current_user):
            data_order = {
                'id_product': order['product']['id'],
                'id_user': order['id_user'],
                'status': form.state.data,
                'price': order['price'],
                'create_date': order['create_date'],
            }
            resp = put(f'http://localhost:5000/api/orders/{order_id}', json=data_order)
            if resp.status_code == 200:
                return redirect(f'/order/{order_id}')

        if 'delete_submit' in request.form and current_user.role_id == 4:
            tokn = generate_token({'id': current_user.id})
            req = delete(f'http://localhost:5000/api/orders/{order_id}',
                         headers={'Authorization': 'Bearer ' + tokn})
            if req.status_code == 200:
                return redirect(f'/admin/orders')
    if order['id_user'] != current_user.id and not check_if_support(current_user):
        return render_template('fail.html', message='У вас нет прав на просмотр этого заказа!', errr_code='403')
    return render_template('order.html', order=order, form=form)


@app.route('/profile/<int:user_id>/notifications', methods=['GET', 'POST'])
@login_required
def user_notifications(user_id):
    if current_user.id != user_id and not check_if_admin(current_user):
        return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    if request.method == 'POST':
        if 'delete_submit' in request.form:
            id = request.form.get('delete_submit')
            res = delete(f'http://localhost:5000/api/notification/{id}')

        if 'read_submit' in request.form:
            id = request.form.get('read_submit')
            res = put(f'http://localhost:5000/api/notification/{id}', json={'read': True})
        return redirect(f'/profile/{user_id}/notifications')

    notifications = get(f'http://localhost:5000/api/notification?id_user={user_id}').json()
    return render_template('profile_notifications.html', user_id=user_id, notifications=notifications)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    serve(app, host="0.0.0.0", port=5000)
