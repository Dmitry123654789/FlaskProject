from flask import make_response, jsonify


def bad_request(*fields):
    if fields:
        return make_response(jsonify({'message': f'Неверно переданы аргументы запроса. Поля {", ".join(fields)}'}), 400)
    else:
        make_response(jsonify({'message': f'Неверно переданы аргументы запроса.'}), 400)
