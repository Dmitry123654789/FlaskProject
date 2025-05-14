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
        # print('huh?', request.form, request.data, request.form.to_dict())
        try:
            args = request.form.to_dict()
        except Exception as e:
            BadRequest(str(e))
            # print('error', e)

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
        sess.commit()

        desc_id = new_description.id

        product_folder = os.path.join('static/img/products/', f'product_{desc_id}')
        os.makedirs(product_folder, exist_ok=True)

        files = request.files
        file_num = 1
        for key, file in files.items():
            if file and allowed_file(file.filename):
                fileext = file.filename.split('.')[-1]
                file_path = os.path.join(product_folder, f'{file_num}.{fileext}')
                file_num += 1
                file.save(file_path)

        new_product = Product(
            price=args['price'],
            discount=args['discount'],
            title=args['title'],
            id_description=desc_id,
            path_images=product_folder
        )
        sess.add(new_product)
        sess.commit()
        return jsonify({'message': 'success', 'id': new_product.id}, 200)

    def put(self):
        try:
            args = request.form.to_dict()
        except Exception as e:
            raise BadRequest()

        if not 'description_id' in request.args.keys() or not request.args['description_id'].isdigit() or \
                not 'product_id' in request.args.keys() or not request.args['product_id'].isdigit():
            raise BadRequest()
        sess = db_session.create_session()
        desc = sess.get(DescriptionProduct, request.args['description_id'])
        prod = sess.get(Product, request.args['product_id'])

        for key in ['description', 'size', 'type', 'material', 'color', 'style', 'features']:
            setattr(desc, key, args[key])

        for key in ['price', 'discount', 'title']:
            setattr(prod, key, args[key])
        setattr(prod, 'id_description', request.args['description_id'])
        sess.commit()


        product_folder = os.path.join('static/img/products/', f'product_{request.args["description_id"]}')
        files = request.files

        if list(files.values())[0].filename != '':
            for f in os.listdir(product_folder):
                os.remove(product_folder + '/'+ f   )
        os.makedirs(product_folder, exist_ok=True)


        file_num = 1
        for key, file in files.items():
            if file and allowed_file(file.filename):
                fileext = file.filename.split('.')[-1]
                file_path = os.path.join(product_folder, f'{file_num}.{fileext}')
                file_num += 1
                file.save(file_path)

        return jsonify({'message': 'success', 'id': int(request.args['description_id'])}, 200)
