from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Employee, ProductSeries, ProductType, Product, Event, Sale

class UserModelCase(unittest.TestCase):
    def setUp(self):
        current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_user(self):

        # Make sure all 4 fields are required to create a User
        self.assertFalse(User(first_name='bryan', last_name='owen', password_hash='asdf'))
        self.assertFalse(User(username='bowen', last_name='owen', password_hash='asdf'))
        self.assertFalse(User(username='bowen', first_name='bryan', password_hash='asdf'))
        self.assertFalse(User(username='bowen', first_name='bryan', last_name='owen'))

        # Make sure a new User holds state correctly
        u = User(username='bryandowen', first_name='bryan', last_name='owen', password_hash='asdf')
        self.assertTrue(u.username='bryandowen')
        self.assertTrue(u.first_name='bryan')
        self.assertTrue(u.last_name='owen')
        self.assertTrue(u.password_has='asdf')

    def test_event():
        e = Event()

    def test_product_series():
        ps = ProductSeries()
