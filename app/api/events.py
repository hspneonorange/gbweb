from app.api import bp
from flask import jsonify, request, url_for
from app.models import Event
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/events/<int:id>', methods=['GET'])
@token_auth.login_required
def get_event(id):
    return jsonify(Event.query.get_or_404(id).to_dict())

@bp.route('/events', methods=['GET'])
@token_auth.login_required
def get_events():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = Event.to_collection_dict(Event.query.order_by(Event.end_date.desc()), page, per_page, 'api.get_events')
    return jsonify(data)

@bp.route('/events', methods=['POST'])
@token_auth.login_required
def create_event():
    data = request.get_json() or {}
    if 'name' not in data or 'city' not in data or 'state_abbr' not in data:
        return bad_request('Must include event name, city, and state name abbreviation.')
    if Event.query.filter_by(name=data['name']).first():
        return bad_request('Another event already has the same name. To avoid confusion, please add the year.')
    event = Event()
    event.from_dict(data)
    db.session.add(event)
    db.session.commit()
    response = jsonify(event.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_event', id=event.id)
    return response

@bp.route('/events/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != event.name and Event.query.filter_by(name=data['name']).first():
        return bad_request('Another event already has the same name. To avoid confusion, please add the year.')
    event.from_dict(data)
    db.session.commit()
    return jsonify(event.to_dict())

@bp.route('/events/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return '', 204
