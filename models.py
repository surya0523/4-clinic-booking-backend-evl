from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, date

# Flask-Login-க்கு தேவையான யூசரை லோட் செய்யும் Function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_doctor = db.Column(db.Boolean, default=False)

    doctor = db.relationship('Doctor', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    
    slots = db.relationship('Slot', backref='doctor', lazy=True)

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    
    booking = db.relationship('Booking', backref='slot', uselist=False)

    def __repr__(self):
        return f"Slot({self.doctor.user.username}, {self.start_time.strftime('%Y-%m-%d %H:%M')}, Booked: {self.is_booked})"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booked_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('User', backref='bookings')