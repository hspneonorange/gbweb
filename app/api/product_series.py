from app.api import bp
from flask import jsonify, request, url_for
from app.models import ProductSeries
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/product_series/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_product_series(id):
    return jsonify(ProductSeries.query.get_or_404(id).to_dict())

@bp.route('/product_series', methods=['GET'])
#@token_auth.login_required
def get_series():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = ProductSeries.to_collection_dict(ProductSeries.query, page, per_page, 'api.get_series')
    return jsonify(data)

@bp.route('/product_series', methods=['POST'])
#@token_auth.login_required
def create_product_series():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('Must include product series name.')
    if ProductSeries.query.filter_by(name=data['name']).first():
        return bad_request('Another series already has this name.')
    product_series = ProductSeries()
    product_series.from_dict(data)
    db.session.add(product_series)
    db.session.commit()
    response = jsonify(product_series.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_product_series', id=product_series.id)
    return response

@bp.route('/product_series/<int:id>', methods=['PUT'])
#@token_auth.login_required
def update_product_series(id):
    product_series = ProductSeries.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != product_series.name and ProductSeries.query.filter_by(name=data['name']).first():
        return bad_request('Another series already has this name.')
    product_series.from_dict(data)
    db.session.commit()
    return jsonify(product_series.to_dict())