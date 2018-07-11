"""Defines the Flask application"""
from app.models import User, Event, Sale, ProductSeries, ProductType, Product, SalesLineItem
from app import app, db

@app.shell_context_processor
def make_shell_context():
    """Prepare the flask shell context so it is already aware of the entire data model"""
    return {'db': db, 'User': User, 'Event': Event, 'Sale': Sale, \
        'ProductSeries': ProductSeries, 'ProductType': ProductType, \
        'Product': Product, 'SalesLineItem': SalesLineItem}
