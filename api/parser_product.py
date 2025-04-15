from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('price', required=True, type=int)
parser.add_argument('discount', required=True, type=int)
parser.add_argument('title', required=True, type=str)
parser.add_argument('path_images', required=True, type=str)