import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page'
bootstrap = Bootstrap(app)
moment = Moment(app)
admin = Admin(app, name='Glasses Brigade', template_mode='bootstrap3')

from app.models import User, Event, Sale, ProductSeries, ProductType, Product, SaleLineItem, Commission, Expense
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Sale, db.session))
admin.add_view(ModelView(ProductSeries, db.session))
admin.add_view(ModelView(ProductType, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(SaleLineItem, db.session))
admin.add_view(ModelView(Commission, db.session))
admin.add_view(ModelView(Expense, db.session))

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp, url_prefix='/errors')

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, gbforms

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/gbweb.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('gbweb startup')
