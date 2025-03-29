from Tools.scripts.make_ctype import method
from flask import Flask, render_template, session
from flask_login import login_required, LoginManager, current_user, user_unauthorized
from jinja2.ext import debug

from user_form import UserForm

app = Flask(__name__)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    order = {'status': 'done', 'name': 'Шкаф-купе 175x75', 'price': 56500, 'id': 1}
    return render_template('profile.html', user_id=user_id, order=order)


@app.route('/profile/<int:user_id>/info', methods=['GET', 'POST'])
def user_info(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    form = UserForm()
    # if method == 'GET':
    #  TODO: подключение к БД и получение информации о пользователе
    # user = db_session.get(User, user_id)
    #
    # form.phone_number.data = user.phone_number
    # form.email.data = user.email
    # form.surname.data = user.surname
    # form.name.data = user.name
    # form.patronymic.data = user.patronymic
    # form.birth_date.data = user.birth_date
    # form.sex.data = user.sex
    # form.address.data = user.address

    # if form.validate_on_submit():
    #     #  TODO: подключение к БД и получение информации о пользователе
    #     # user = db_session.get(User, user_id)
    #     if user:
    #         user.phone_number = form.phone_number.data
    #         user.email = form.email.data
    #         user.surname = form.surname.data
    #         user.name = form.name.data
    #         user.patronymic = form.patronymic.data
    #         user.birth_date = form.birth_date.data
    #         user.sex = form.sex.data
    #         user.address = form.address.data
    return render_template('profile_info.html', user_id=user_id, form=form)


@app.route('/profile/<int:user_id>/orders')
def user_orders(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    orders = [{'status': 'sent', 'name': 'Шкаф-купе 175x100', 'price': 120000, 'id': 1},
              {'status': 'done', 'name': 'Шкаф-купе 50x75', 'price': 43900, 'id': 2},
              {'status': 'construction', 'name': 'Шкаф-купе 175x75', 'price': 210000, 'id': 3}]
    return render_template('profile_orders.html', user_id=user_id, orders=orders)


@app.route('/profile/<int:user_id>/notifications')
def user_notifications(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
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


@app.route('/profile/<int:user_id>/login')
def login(user_id):
    pass


@app.route('/profile/<int:user_id>/logout')
def logout(user_id):
    pass


@app.route('/test')
def test():
    notifications = [
        {
            'title': 'Новая акция!',
            'text': 'Скидка 20% на все товары до конца недели.dddcfg hhyy. hhyy. dassww! ddwwr? dada daaaad dddda w wwerrr fada',
            'date_short': '29 мар',
            'date_full': '29 марта 2025',
            'read': True
        }]
    return render_template('notifications.html', notifications=notifications)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')
