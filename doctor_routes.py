from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from .models import Slot, Doctor, Booking
from .app import db
from datetime import datetime, timedelta

doctor_bp = Blueprint('doctor_bp', __name__)

# Custom decorator to check if the current user is a doctor
def doctor_required(f):
    @login_required
    def wrap(*args, **kwargs):
        if not current_user.is_doctor:
            flash('Access denied. Doctors only.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@doctor_bp.route('/dashboard')
@doctor_required
def dashboard():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    # Get all upcoming slots and bookings for the doctor
    upcoming_slots = Slot.query.filter(
        Slot.doctor == doctor, 
        Slot.start_time >= datetime.utcnow()
    ).order_by(Slot.start_time).all()
    
    return render_template('doctor/dashboard.html', slots=upcoming_slots)

@doctor_bp.route('/manage_slots', methods=['GET', 'POST'])
@doctor_required
def manage_slots():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        # Logic to add new slots (e.g., date, start_time, duration)
        # 1. Parse date and time from form
        # 2. Create new Slot objects (e.g., Slot(doctor_id=doctor.id, start_time=new_dt))
        # 3. db.session.add_all() and db.session.commit()
        flash('New slots added successfully!', 'success')
        return redirect(url_for('doctor_bp.dashboard'))
        
    return render_template('doctor/manage_slots.html')

# Slot deletion route (optional)
@doctor_bp.route('/slot/delete/<int:slot_id>', methods=['POST'])
@doctor_required
def delete_slot(slot_id):
    # Logic to delete a slot if it's not booked
    return redirect(url_for('doctor_bp.dashboard'))