from app.api import bp
from flask import jsonify, request, url_for
from app.models import SaleLineItem
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/sale_line_items/<int:id>', methods=['GET'])
@token_auth.login_required
def get_sale_line_item(id):
    return jsonify(SaleLineItem.query.get_or_404(id).to_dict())

@bp.route('/sale_line_items', methods=['GET'])
@token_auth.login_required
def get_sale_line_items():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = SaleLineItem.to_collection_dict(SaleLineItem.query, page, per_page, 'api.get_sale_line_items')
    return jsonify(data)

@bp.route('/sale_line_items', methods=['POST'])
@token_auth.login_required
def create_sale_line_item():
    data = request.get_json() or {}
    print(data)
    if 'product_id' not in data or 'sale_id' not in data or 'sale_price' not in data or 'num_sold' not in data:
        return bad_request('Must include product_id, sale_id, and sale_price fields.')
    sli = SaleLineItem()
    sli.from_dict(data)
    db.session.add(sli)
    db.session.commit()
    # Decrement stock in products table by [num_sold]
    response = jsonify(sli.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_sale_line_item', id=sli.id)
    return response

@bp.route('/sale_line_items/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_sale_line_item(id):
    sli = SaleLineItem.query.get_or_404(id)
    data = request.get_json() or {}
    sli.from_dict(data)
    db.session.commit()
    return jsonify(sli.to_dict())
