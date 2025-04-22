from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('id', type=str, required=True, help="Surname cannot be blank!")
user_parser.add_argument('id_user', type=str, required=True, help="Name cannot be blank!")
user_parser.add_argument('theme', type=str)
user_parser.add_argument('question', type=str, required=True, help="Email cannot be blank!")