from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True)
parser.add_argument('text', type=str, required=True)
parser.add_argument('public', type=bool, required=True)
parser.add_argument('read', type=bool, required=True)
parser.add_argument('create_date', required=True)
parser.add_argument('id_user', type=int, required=True)