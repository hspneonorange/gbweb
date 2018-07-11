"""Model for the ORM layer"""
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db

@login.user_loader
def load_user(id):
    """Satisfies the flask_login requirement to have a user_loader"""
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    """Represents a login user for the application"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sales = db.relationship('Sale', backref='user', lazy='dynamic')
    def __repr__(self):
        return '<Employee {}: {}, {}>'.format(self.username, self.last_name, self.first_name)
    def set_password(self, password):
        """Hashes the provided password, and stores it in object state"""
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        """Hashes the provided password and compares it to the password hash in object state"""
        return check_password_hash(self.password_hash, password)

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
