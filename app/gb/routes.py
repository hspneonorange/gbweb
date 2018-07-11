from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User

@bp.route('/admin', methods=['GET', 'POST'])
@login_required
