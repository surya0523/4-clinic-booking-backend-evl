from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from .models import User, Doctor, Slot, Booking
from .forms import RegistrationForm, LoginForm, BookingForm # Forms need to be created
from .app import db

main = Blueprint('main', __name__)

# Utility function (needs to be implemented in a separate utility file)
# from .utils import send_email_notification 

@main.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.is_doctor:
            return redirect(url_for('doctor_bp.dashboard'))
        return redirect(url_for('main.book_appointment'))
    return render_template('patient/home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic (User creation, password hashing, db.session.add)
    # Use RegistrationForm
    return render_template('patient/register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic (check_password, login_user)
    # Use LoginForm
    return render_template('patient/login.html')

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

@main.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = BookingForm()
    doctors = Doctor.query.all()
    
    # Form logic:
    # 1. Fetch available slots based on selected doctor (using AJAX/JS or form submit)
    # 2. On form submission:
    #    a. Check if slot is available (is_booked=False)
    #    b. Create new Booking object
    #    c. Update Slot: slot.is_booked = True
    #    d. db.session.commit()
    #    e. send_email_notification (Booking confirmation)
    # 3. Flash success message and redirect.

    return render_template('patient/book.html', form=form, doctors=doctors)