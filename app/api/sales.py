from app.api import bp
from flask import jsonify, request, url_for
from app.models import Sale
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/sales/<int:id>', methods=['GET'])
@token_auth.login_required
def get_sale(id):
    return jsonify(Sale.query.get_or_404(id).to_dict())

@bp.route('/sales', methods=['GET'])
@token_auth.login_required
def get_sales():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Sale.to_collection_dict(Sale.query, page, per_page, 'api.get_sales')
    return jsonify(data)

@bp.route('/sales/<int:user_id>/<int:event_id>', methods=['GET'])
@token_auth.login_required
def get_user_event_sales(user_id, event_id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = Sale.to_collection_dict(Sale.query.filter(Sale.user_id == user_id).filter(Sale.event_id == event_id), page, per_page, 'api.get_user_event_sales', user_id=user_id, event_id=event_id)
    return jsonify(data)

@bp.route('/sales', methods=['POST'])
@token_auth.login_required 
def create_sale():
    data = request.get_json() or {}
    if 'event_id' not in data or 'user_id' not in data or 'date' not in data:
        return bad_request('Must include event_id, user_id, and date fields.')
    sale = Sale()
    sale.from_dict(data)
    db.session.add(sale)
    db.session.commit()
    response = jsonify(sale.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_sale', id=sale.id)
    return response

@bp.route('/sales/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_sale(id):
    sale = Sale.query.get_or_404(id)
    data = request.get_json() or {}
    sale.from_dict(data)
    db.session.commit()
    return jsonify(sale.to_dict())

@bp.route('/sales/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_sale(id):
    sale = Sale.query.get_or_404(id)
    db.session.delete(sale)
    db.session.commit()
    return '', 204
