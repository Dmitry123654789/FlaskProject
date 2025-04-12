from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id_product', required=True, type=int)
parser.add_argument('description', required=True, type=str)