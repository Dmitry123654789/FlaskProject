from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('description', required=True, type=str)
parser.add_argument('size', required=True, type=str)
parser.add_argument('type', required=True, type=str)
parser.add_argument('material', required=True, type=str)
parser.add_argument('color', required=True, type=str)
parser.add_argument('style', required=True, type=str)
parser.add_argument('features', required=True, type=str)