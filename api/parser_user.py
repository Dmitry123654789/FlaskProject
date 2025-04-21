from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('surname', type=str, required=True, help="Surname cannot be blank!")
user_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
user_parser.add_argument('phone', type=str)
user_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
user_parser.add_argument('patronymic', type=str)
user_parser.add_argument('birth_date', type=str)
user_parser.add_argument('sex', type=str)
