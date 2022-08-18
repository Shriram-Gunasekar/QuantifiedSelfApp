from . import db
from .models import Account, Trackers, Info

from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for

views = Blueprint('views', __name__, url_defaults=None, root_path=None ) #template_folder not specified

@views.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user, trackers=Trackers().query.filter_by(user_id=current_user.id).all())

@views.route('/create_tracker', methods=['GET', 'POST'])
@login_required
def create_tracker():
    if request.method == 'POST':
        tracker_name = request.form.get('t_name')
        tracker_type = request.form.get('t_type')
        tracker_note = request.form.get('t_note')
        check = Trackers.query.filter_by(t_name=tracker_name, user_id=current_user.id).first()
        if check:
            flash('Tracker already exists! Use a different name', category='error')
            return render_template('create_tracker.html', user=current_user)
        else:
            new_tracker = Trackers(t_name=tracker_name, t_type=tracker_type, t_note=tracker_note, user_id=current_user.id)
            db.session.add(new_tracker)
            db.session.commit()
            flash('Tracker created!', category='success')
    return render_template('create_tracker.html', user=current_user)  

@views.route('/delete_tracker/<int:tracker_id>', methods=['GET','POST'])
@login_required
def delete_tracker(tracker_id):        
    tracker = Trackers.query.filter_by(id=tracker_id, user_id = current_user.id).first()
    db.session.delete(tracker)
    tracker = Info.query.filter_by(t_id=tracker_id, user_id = current_user.id).all()
    if tracker:
        for i in tracker:
            db.session.delete(i)
    db.session.commit()
    flash('Tracker deleted!', category='success')
        
    return redirect(url_for('views.dashboard'))

@views.route('/update_tracker/<int:tracker_id>', methods=['GET','POST'])
@login_required
def update_tracker(tracker_id):
    if request.method == 'POST':
        notevalue = request.form.get('t_note') 
        namevalue = request.form.get('t_name')
        tracker = Trackers.query.filter_by(id=tracker_id, user_id = current_user.id).first()
        tracker.t_note = notevalue
        tracker.t_name = namevalue
        db.session.commit()
        flash('Tracker updated!', category='success')
    return render_template('updatetracker.html', user=current_user, trackers=Trackers().query.filter_by(user_id=current_user.id).all())



@views.route('/view_tracker/<int:tracker_id>', methods=['GET','POST'])
@login_required
def view_tracker(tracker_id):      
    if request.method == 'POST':
        entervalue = request.form.get('info_value') 
        
        new_info = Info(t_value=entervalue, t_id=tracker_id, user_id=current_user.id)
        db.session.add(new_info)
        db.session.commit() 
        flash('Info added!', category='success')
    data=Info().query.filter_by(t_id=tracker_id, user_id = current_user.id).all()
    tracker_type = Trackers.query.filter_by(id=tracker_id, user_id = current_user.id).first().t_type
    labels = []
    values = []
    if(tracker_type == 'Boolean'):
        labels = [str(info.t_date) for info in data]
        values = [ 0 if info.t_value == 0 else 1 for info in data ]
    if(tracker_type == 'Numeric'):
        labels = [str(info.t_date) for info in data]
        values = [info.t_value for info in data ]
        
        
    return render_template ('viewtracker.html', 
                           user=current_user, 
                           info=Info().query.filter_by(t_id=tracker_id, user_id = current_user.id).all(),
                           labels=labels,
                           values=values,       
                           trackername = Trackers.query.filter_by(id=tracker_id, user_id = current_user.id).first().t_name,
                           trackernote = Trackers.query.filter_by(id=tracker_id, user_id = current_user.id).first().t_note,
                           trackertype = Trackers.query.filter_by(id=tracker_id, user_id = current_user.id).first().t_type
                           )

@views.route('/view_tracker/delete_info/<int:i_id>', methods=['GET','POST'])
@login_required
def delete_info(i_id):
    info = Info.query.filter_by(id=i_id, user_id = current_user.id).first()
    db.session.delete(info)
    db.session.commit()
    flash('Info deleted!', category='success')
    tracker_id=info.t_id
    return redirect(url_for('views.view_tracker', tracker_id=tracker_id))
    
@views.route('/view_tracker/edit_info/<int:info_id>', methods=['GET','POST'])
def edit_info(info_id):
    if request.method == 'POST':
        entervalue = request.form.get('info_value') 
        info = Info.query.filter_by(id=info_id, user_id = current_user.id).first()
        info.t_value = entervalue
        db.session.commit()
        flash('Info updated!', category='success')
    return render_template ('editinfo.html', user=current_user, info=Info.query.filter_by(id=info_id, user_id = current_user.id).first())
    
      





