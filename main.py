from flask import Flask, render_template, session
from flask_login import login_required, LoginManager, current_user, user_unauthorized

app = Flask(__name__)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    order = {'status': 'done', 'name': 'Шкаф-купе 175x75', 'price': 56500, 'id': 1}
    return render_template('profile.html', user_id=user_id, order=order)


@app.route('/profile/<int:user_id>/info')
def user_info(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    return render_template('profile_info.html', user_id=user_id)


@app.route('/profile/<int:user_id>/orders')
def user_orders(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    return render_template('profile_orders.html', user_id=user_id)


@app.route('/profile/<int:user_id>/questions')
def user_questions(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    return render_template('profile_questions.html', user_id=user_id)


@app.route('/profile/<int:user_id>/notifications')
def user_notifications(user_id):
    # if user_unauthorized or current_user.id != user_id and current_user.id not in admin_ids:
    #     return render_template('fail.html', message='У вас нет прав на просмотр профиля другого пользователя')
    return render_template('profile_notifications.html', user_id=user_id)

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


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')
