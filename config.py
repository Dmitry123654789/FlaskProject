import datetime

import jwt

SECRET_KEY = 'yandexlyceum_secret_key'


def generate_token(in_dict: dict, expie_time=300):
    payload = {
        key: value for key, value in in_dict.items()

    }
    payload.update(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expie_time), 'iat': datetime.datetime.utcnow()})
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
