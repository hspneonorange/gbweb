from app.api import bp
from flask import jsonify, request, url_for
from app.models import Product, SaleLineItem, Sale
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth
import simplejson as json

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
        data = Product.to_collection_dict(Product.query.filter(Product.keywords.like("%" + search + "%")), page, per_page, 'api.get_products')
    else:
        data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_products')
    return jsonify(data)

@bp.route('/products/id_search', methods=['GET'])
@token_auth.login_required
def get_products_by_id():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search_id = request.args.get('search', None, type=str)
    if search_id != "":
        data = Product.to_collection_dict(Product.query.filter(Product.id.like(search_id)), page, per_page, 'api.get_products')
    else:
        data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_products')
    return jsonify(data)

@bp.route('/products/low_stock', methods=['GET'])
@token_auth.login_required
def get_products_by_stock():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    data = Product.to_collection_dict(Product.query.order_by(Product.stock, Product.product_series_id, Product.name).filter(Product.product_type_id==1), page, per_page, 'api.get_products')
    return jsonify(data)

@bp.route('/products/top_sellers/<int:event_id>', methods=['GET'])
@token_auth.login_required
def get_top_sellers_by_event(event_id):
    top_sellers = db.session.execute('select p.id, p.name, sum(num_sold) as ''num_sold'' from event e join sale s on e.id = s.event_id join sale_line_item sli on s.id = sli.sale_id join product p on sli.product_id = p.id where e.id = 14 group by p.id, p.name order by sum(num_sold) desc, p.name limit 50;').fetchall()
    for row in top_sellers:
        print(row)

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

@bp.route('/products/stock/<int:product_id>/<int:stock_update>', methods=['PUT'])
@token_auth.login_required
def update_stock(product_id, stock_update):
    action = request.args.get('action', None, type=str)
    product = Product.query.get_or_404(product_id)
    if action == 'increment':
        product.stock += stock_update
    elif action == 'decrement':
        product.stock -= stock_update
    else:
        print('This should never happen')
    db.session.commit()
    return jsonify(product.stock, product.to_dict())

@bp.route('/products/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
