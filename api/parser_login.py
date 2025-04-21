from flask_restful import reqparse

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
login_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
