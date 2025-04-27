from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id_product', required=True, type=int)
parser.add_argument('id_user', required=True, type=int)
parser.add_argument('status', required=True, type=bool)
parser.add_argument('price', required=True, type=int)
parser.add_argument('create_date', required=True, type=str)