import os

from flask import jsonify, session
from flask_restful import Resource
from flask import request
from werkzeug.exceptions import NotFound, BadRequest

from data.product import Product
from .parser_full_product import product_parser
from data import db_session
from data.description_product import DescriptionProduct

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class FullProductResource(Resource):
    def post(self):
        print('huh?', request.files, request.files.getlist('images'))
        args = product_parser.parse_args()

        sess = db_session.create_session()

        new_description = DescriptionProduct(
            description=args['description'],
            size=args['size'],
            type=args['type'],
            material=args['material'],
            color=args['color'],
            style=args['style'],
            features=args['features']
        )

        sess.add(new_description)

        desc_id = new_description.id
        print('yo!')
        product_folder = os.path.join('static/img/products/', f'product_{desc_id}')
        os.makedirs(product_folder, exist_ok=True)

        try:

            files = request.files.getlist('images')
        except Exception as e:
            print(e)


        for idx, file in enumerate(files):
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{idx}.{ext}"
                filepath = os.path.join(product_folder, filename)
                file.save(filepath)

        print(product_folder)
        new_product = Product(
            price=args['price'],
            discount=args['discount'],
            title=args['title'],
            id_description=desc_id,
            path_images=product_folder
        )
        sess.add(new_product)
