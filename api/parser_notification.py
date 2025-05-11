from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('text', type=str)
parser.add_argument('read', type=bool)
parser.add_argument('create_date')
parser.add_argument('id_user', type=int)