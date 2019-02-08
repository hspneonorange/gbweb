from app.api import bp
from flask import jsonify, request, url_for
from app.models import Product
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/products/<int:id>', methods=['GET'])
@token_auth.login_required
def get_product(id):
    return jsonify(Product.query.get_or_404(id).to_dict())

@bp.route('/products', methods=['GET'])
@token_auth.login_required
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search = request.args.get('search', None, type=str)
    if search != "":
        print("HEY!!!")
        data = Product.to_collection_dict(Product.query.filter(Product.keywords.like("%" + search + "%")), page, per_page, 'api.get_products')
#        data = Product.to_collection_dict(Product.query.filter_by(Product.keywords.like("%" + search + "%")), page, per_page, 'api.get_products')
    else:
        data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_products')
    return jsonify(data)

@bp.route('/products', methods=['POST'])
@token_auth.login_required
def create_product():
    data = request.get_json() or {}
    if 'product_type_id' not in data or 'product_series_id' not in data or 'name' not in data or 'stock' not in data or 'price' not in data:
        return bad_request('Must include product_series_id, product_type_id, name, stock, and price fields.')
    product = Product()
    product.from_dict(data)
    db.session.add(product)
    db.session.commit()
    response = jsonify(product.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_product', id=product.id)
    return response

@bp.route('/products/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json() or {}
    product.from_dict(data)
    db.session.commit()
    return jsonify(product.to_dict())

@bp.route('/products/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
