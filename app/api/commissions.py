from app.api import bp
from flask import jsonify, request, url_for
from app.models import Commission
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/commissions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_commission(id):
    return jsonify(Commission.query.get_or_404(id).to_dict())

@bp.route('/commissions', methods=['GET'])
@token_auth.login_required
def get_commissions():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Commission.to_collection_dict(Commission.query, page, per_page, 'api.get_commissions')
    return jsonify(data)

@bp.route('/commissions', methods=['POST'])
@token_auth.login_required
def create_commission():
    data = request.get_json() or {}
    if 'event_id' not in data or 'user_id' not in data or 'price' not in data or 'datetime_recorded' not in data or 'commissioner_name' not in data or 'commissioner_email' not in data or 'commission_details' not in data or 'price' not in data:
        return bad_request('Must include product_id, sale_id, and sale_price fields.')
    c = Commission()
    c.from_dict(data)
    db.session.add(c)
    db.session.commit()
    response = jsonify(c.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_commission', id=c.id)
    return response

@bp.route('/commissions/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_commission(id):
    sli = Commission.query.get_or_404(id)
    data = request.get_json() or {}
    c.from_dict(data)
    db.session.commit()
    return jsonify(c.to_dict())
