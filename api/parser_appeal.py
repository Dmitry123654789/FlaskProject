from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', type=str, required=True, help="Surname cannot be blank!")
parser.add_argument('id_user', type=str, required=True, help="Name cannot be blank!")
parser.add_argument('theme', type=str)
parser.add_argument('question', type=str, required=True, help="Email cannot be blank!")