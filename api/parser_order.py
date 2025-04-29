from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id_product', type=int)
parser.add_argument('id_user', type=int)
parser.add_argument('status', type=str)
parser.add_argument('price', type=int)
parser.add_argument('create_date', type=str)