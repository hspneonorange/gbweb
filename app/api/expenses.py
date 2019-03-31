from app.api import bp
from flask import jsonify, request, url_for
from app.models import Expense
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/expenses/<int:id>', methods=['GET'])
@token_auth.login_required
def get_expense(id):
    return jsonify(Expense.query.get_or_404(id).to_dict())

@bp.route('/expenses', methods=['GET'])
@token_auth.login_required
def get_expenses():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Expense.to_collection_dict(Expense.query, page, per_page, 'api.get_expenses')
    return jsonify(data)

@bp.route('/expenses', methods=['POST'])
@token_auth.login_required
def create_expense():
    print('in create_expense')
    data = request.get_json() or {}
    print('')
    if 'description' not in data or 'cost' not in data or 'user_id' not in data or 'event_id' not in data or 'datetime_recorded' not in data:
        print('bad request')
        return bad_request('Must include description, cost, user_id, event_id, and datetime_recorded fields.')
    expense = Expense()
    print('expense = Expense()')
    expense.from_dict(data)
    print('expense.from_dict')
    db.session.add(expense)
    print('session.add(expense)')
    db.session.commit()
    print('session.commit')
    response = jsonify(expense.to_dict())
    print('jsonify response')
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_expense', id=expense.id)
    return response

@bp.route('/expenses/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_expense(id):
    expense = Expense.query.get_or_404(id)
    data = request.get_json() or {}
    expense.from_dict(data)
    db.session.commit()
    return jsonify(expense.to_dict())

@bp.route('/expenses/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return '', 204
