from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id_user', type=int, required=True)
parser.add_argument('theme', type=str, required=True)
parser.add_argument('question', type=str, required=True)