from flask_restful import reqparse

product_parser = reqparse.RequestParser()
product_parser.add_argument('price', required=True, type=int)
product_parser.add_argument('discount', required=True, type=int)
product_parser.add_argument('title', required=True, type=str)
product_parser.add_argument('description', required=True, type=str)
product_parser.add_argument('size', required=True, type=str)
product_parser.add_argument('type', required=True, type=str)
product_parser.add_argument('material', required=True, type=str)
product_parser.add_argument('color', required=True, type=str)
product_parser.add_argument('style', required=True, type=str)
product_parser.add_argument('features', required=True, type=str)