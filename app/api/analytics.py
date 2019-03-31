from app.api import bp
from flask import jsonify, request, url_for
from app.models import Sale, SaleLineItem, Event
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/analytics/<int:event_id>', methods=['GET'])
@token_auth.login_required
def get_analytics(event_id):

    sales = Sale.query.filter(Sale.event_id == event_id).join(Sale.salelineitems).with_entities(SaleLineItem.sale_price.label('sale_price'), SaleLineItem.num_sold.label('num_sold')).all()
    discounts = Sale.query.filter(Sale.event_id == event_id).with_entities(Sale.discount.label('discount')).all()

    total_sales = sum(s.sale_price * s.num_sold for s in sales)
    total_discounts = sum(d.discount for d in discounts)
    r = {
        'total': total_sales - total_discounts
    }
    return jsonify(r)
