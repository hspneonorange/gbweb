#from wtforms_alchemy import ModelForm
from wtforms_alchemy import model_form_factory
from wtforms import SubmitField
from flask_wtf import FlaskForm
from app.models import User, Event, Sale, ProductType, ProductSeries, Product, SaleLineItem, Commission

ModelForm = model_form_factory(FlaskForm)

class UserForm(ModelForm):
    class Meta:
        model = User

class EventForm(ModelForm):
    class Meta:
        model = Event

class SaleForm(ModelForm):
    class Meta:
        model = Sale

class ProductTypeForm(ModelForm):
    class Meta:
        model = ProductType

class ProductSeriesForm(ModelForm):
    class Meta:
        model = ProductSeries

class ProductForm(ModelForm):
    class Meta:
        model = Product

class SaleLineItemForm(ModelForm):
    class Meta:
        model = SaleLineItem

class CommissionForm(ModelForm):
    class Meta:
        model = Commission
