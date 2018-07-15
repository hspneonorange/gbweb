from app.api import bp
from flask import jsonify, request, url_for
from app.models import ProductType
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/product_types/<int:id>', methods=['GET'])
@token_auth.login_required
def get_product_type(id):
    return jsonify(ProductType.query.get_or_404(id).to_dict())

@bp.route('/product_types', methods=['GET'])
@token_auth.login_required
def get_product_types():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = ProductType.to_collection_dict(ProductType.query, page, per_page, 'api.get_product_types')
    return jsonify(data)

@bp.route('/product_types', methods=['POST'])
@token_auth.login_required
def create_product_type():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('Must include product type name.')
    if ProductType.query.filter_by(name=data['name']).first():
        return bad_request('Another product type already has the same name.')
    product_type = ProductType()
    product_type.from_dict(data)
    db.session.add(product_type)
    db.session.commit()
    response = jsonify(product_type.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_product_type', id=product_type.id)
    return response

@bp.route('/product_types/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_product_type(id):
    product_type = ProductType.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != product_type.name and ProductType.query.filter_by(name=data['name']).first():
        return bad_request('Another product type already has the same name.')
    product_type.from_dict(data)
    db.session.commit()
    return jsonify(product_type.to_dict())