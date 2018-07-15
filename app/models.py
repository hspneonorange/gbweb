"""Model for the ORM layer"""
from flask import url_for
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
import base64
from datetime import datetime, timedelta
import os

@login.user_loader
def load_user(id):
    """Satisfies the flask_login requirement to have a user_loader"""
    return User.query.get(int(id))

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, pper_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(PaginatedAPIMixin, UserMixin, db.Model):
    """Represents a login user for the application"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    sales = db.relationship('Sale', backref='user', lazy='dynamic')
    def __repr__(self):
        return '<Employee {}: {}, {}>'.format(self.username, self.last_name, self.first_name)
    def set_password(self, password):
        """Hashes the provided password, and stores it in object state"""
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        """Hashes the provided password and compares it to the password hash in object state"""
        return check_password_hash(self.password_hash, password)
    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        return data
    def from_dict(self, data, new_user=False):
        for field in ['first_name', 'last_name', 'username']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
    
    token_duration_in_seconds=43200 #12 hrs x 60 min x 60 sec
    def get_token(self, expires_in=token_duration_in_seconds):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class Event(db.Model):
    """Represents an industry event where sales may occur"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    city = db.Column(db.String(50), index=True)
    state_abbr = db.Column(db.String(2), index=True)
    sales = db.relationship('Sale', backref='event', lazy='dynamic')
    def __repr__(self):
        return '<Event {}: {}, {} @ {}-{}>'.format(self.name, self.city, \
            self.state_abbr, self.start_date, self.end_date)

class Sale(db.Model):
    """Models a 'sale' as an abstract entity, to which one or more SaleLineItems are attached"""
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    discount = db.Column(db.Numeric(7, 2))
    notes = db.Column(db.String(256))
    saleslineitems = db.relationship('SaleLineItem', backref='sale', lazy='dynamic')
    def __repr__(self):
        return '<Sale {}, {}>'.format(self.id, self.date)

class ProductType(db.Model):
    """The type of a product - e.g., button, earring, etc."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    products = db.relationship('Product', backref='product_type', lazy='dynamic')
    def __repr__(self):
        return '<ProductType {}>'.format(self.name)

class ProductSeries(db.Model):
    """The series a product is assocaited with - e.g., Sailor Moon, Yu-Gi-Oh!, etc."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    products = db.relationship('Product', backref='product_series', lazy='dynamic')
    def __repr__(self):
        return '<ProductSeries {}>'.format(self.name)

class Product(db.Model):
    """The intersection of a ProductType and ProductSeries; has its own stock count and price"""
    id = db.Column(db.Integer, primary_key=True)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable=False)
    product_series_id = db.Column(db.Integer, db.ForeignKey('product_series.id'), nullable=False)
    name = db.Column(db.String(50), index=True, nullable=False)
    sku = db.Column(db.String(8), index=True)
    description = db.Column(db.String(256))
    notes = db.Column(db.String(1024))
    stock = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Numeric(7, 2), nullable=False)
    saleslineitems = db.relationship('SaleLineItem', backref='product', lazy='dynamic')
    def __repr__(self):
        return '<Product {}, ${}; {} in stock>'.format(self.name, self.price, self.stock)

class SaleLineItem(db.Model):
    """The intersection between a Sale and Products"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    sale_price = db.Column(db.Numeric(7, 2))
    def __repr__(self):
        return '<SaleLineItem {}>'.format(self.id)
