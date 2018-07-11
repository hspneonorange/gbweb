from flask import Blueprint
bp = Blueprint('gb', __name__, template_folder='templtes')

from app import app, models, db
