from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Optional
from app.models import User, Event, ProductSeries, ProductType, Product, Sale, SaleLineItem, Commission

# TODO: Validators for length on every text type field
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    city = StringField('City')
    state_abbr = SelectField('State', [Optional()], choices=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KA', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])

class ProductSeriesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class ProductTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class ProductForm(FlaskForm):
    product_type = SelectField('Product Type', choices=[pt.name for pt in ProductType.query.all()])
    product_series = SelectField('Product Series', choices=[ps.name for ps in ProductSeries.query.all()])
    name = StringField('Name', validators=[DataRequired()])
    sku = StringField('SKU')
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])
    notes = TextAreaField('Notes', validators=[Length(min=0, max=1024)])
    stock = IntegerField('Stock')
    price = FloatField('Price')

class SaleForm(FlaskForm):
    event = SelectField('Event', choices=[e.name for e in Event.query.all()])
    user = SelectField('User', choices=[u.username for u in User.query.all()])
    date = DateField('Sale date', validators=[DataRequired()])
    discount = FloatField('Discount')
    notes = TextAreaField('Notes', validators=[Length(min=0, max=1024)])

class SaleLineItemForm(FlaskForm):
    product_type = SelectField('Product Type', choices=[pt.name for pt in ProductType.query.all()])
    product_type = SelectField('Product Type', choices=[pt.name for pt in ProductType.query.all()])
    sale_price = FloatField('Sale price')