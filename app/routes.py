from app import app
from flask import render_template, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_required
from app.auth import routes
from app import routes, gbforms
from app.gbforms import EventForm
from app.models import Event
import os

@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    return render_template('index.html', title='Home', user=current_user)

@app.route('/images/<path>/<filename>')
def send_image(path, filename):
    #root_dir = os.path.dirname(os.getcwd())
    full_dir = os.path.join(app.root_path.replace('/app', ''), 'images', path)
    print(full_dir)
    return send_from_directory(full_dir, filename)

@app.route('/admin')
@login_required
def admin():
    render_template('admin.html')

@app.route('/crud_event', methods=['GET', 'POST'])
@app.route('/crud_event/<id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def crud_event(id=0):
    form = EventForm()
    if form.validate_on_submit():
        # POST, PUT
        if request.method == 'POST':
            # Create
            e = Event(name=form.name.data, start_date=form.from_date.data, end_date=form.end_date.data, city=form.city.date, state_abbr=form.state_abbr.data)
            db.session.add(e)
            db.session.commit()
            flash('Event created')
            return redirect(url_for('/crud_event'))
        elif request.method == 'PUT':
            # Update
            e = Event.query.filter_by(id=id)
            e.name = form.name.data
            e.start_date = form.start_date.data
            e.end_date = form.end_date.data
            e.city = form.city.data
            e.state_abbr = form.state_abbr.data
            db.session.commit()
            flash('Event updated')
            return redirect(url_for('/crud_event'))
    else:
        if request.method == 'GET':
            if id == 0:
                # Empty form to Create
                return render_template('/crud_event.html', form=form, action='Create', route='event')
            else:
                # Pre-populated form to Update
                form = EventForm(id)
                e = Event.query.filter_by(id=id).first_or_404()
                form.name.data = e.name
                form.start_date.data = e.start_date
                form.end_date.data = e.end_date
                form.city.data = e.city
                form.state_abbr.date = e.state_abbr
                return render_template('/crud_event.html', form=form, action='Update', route='event')
        elif request.method == 'DELETE':
            # Delete
            e = Event.query.filter_by(id=id).first_or_404()
            db.session.delete(e)
            db.session.commit()
            flash('Event deleted')
            return redirect(url_for('/crud_event'))

# GET /crud_event
# GET /crud_event/<id>
# POST /crud_event
# PUT /crud_event/<id>
# DELETE /crud_event/<id>

# generic crud
#    form = Edit<entity>Form()
#    # Create/Update
#    if form.validate_on_submit():
#        model_var = form.<field>.data ...
#        db.session.commit()
#        return redirect(url_for('auth.edit_profile'))
#    elif request.method == 'GET':
#    # Read
#        form.<field>.data = <local_var>
#    return render_template('edit_<entity>.html', title='Edit <Entity>', form=form)
