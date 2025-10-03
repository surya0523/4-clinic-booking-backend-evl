from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "clinic-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'

# Flask-Mail Setup (for reminders)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "your_email@gmail.com"   # <-- Change
app.config['MAIL_PASSWORD'] = "your_password"         # <-- Change
app.config['MAIL_DEFAULT_SENDER'] = "your_email@gmail.com"

db = SQLAlchemy(app)
mail = Mail(app)

# ------------------ MODELS ------------------
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    slots = db.relationship('Slot', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    slot = db.relationship("Slot", backref="appointment", uselist=False)

# ------------------ ROUTES ------------------
@app.route('/')
def index():
    doctors = Doctor.query.all()
    return render_template("index.html", doctors=doctors)

# Book Appointment
@app.route('/book/<int:doctor_id>', methods=["GET", "POST"])
def book(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    slots = Slot.query.filter_by(doctor_id=doctor.id).all()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        slot_id = request.form['slot_id']

        slot = Slot.query.get_or_404(slot_id)

        # Slot already booked?
        if Appointment.query.filter_by(slot_id=slot.id).first():
            flash("This slot is already booked!", "danger")
            return redirect(url_for('book', doctor_id=doctor.id))

        appointment = Appointment(
            patient_name=name,
            email=email,
            slot_id=slot.id,
            doctor_id=doctor.id
        )
        db.session.add(appointment)
        db.session.commit()

        # Send reminder email
        try:
            msg = Message(
                subject="Appointment Confirmation",
                recipients=[email],
                body=f"Dear {name},\n\nYour appointment with Dr. {doctor.name} "
                     f"({doctor.specialization}) is confirmed at {slot.time}.\n\nClinic"
            )
            mail.send(msg)
            flash("Appointment booked & reminder sent!", "success")
        except Exception as e:
            print("Email failed:", e)
            flash("Appointment booked (reminder not sent).", "warning")

        return redirect(url_for('index'))
    return render_template("book.html", doctor=doctor, slots=slots)

# Doctor Dashboard (Manage schedule + view appointments)
@app.route('/doctor/<int:doctor_id>', methods=["GET", "POST"])
def doctor_dashboard(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    slots = Slot.query.filter_by(doctor_id=doctor.id).all()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

    # Add new slot
    if request.method == "POST":
        time = request.form['time']
        new_slot = Slot(time=time, doctor_id=doctor.id)
        db.session.add(new_slot)
        db.session.commit()
        flash("New slot added!", "success")
        return redirect(url_for('doctor_dashboard', doctor_id=doctor.id))

    return render_template("doctor_dashboard.html", doctor=doctor, slots=slots, appointments=appointments)

# Delete slot
@app.route('/doctor/<int:doctor_id>/delete_slot/<int:slot_id>')
def delete_slot(doctor_id, slot_id):
    slot = Slot.query.get_or_404(slot_id)
    if slot.appointment:
        flash("Cannot delete slot - already booked!", "danger")
    else:
        db.session.delete(slot)
        db.session.commit()
        flash("Slot deleted!", "success")
    return redirect(url_for('doctor_dashboard', doctor_id=doctor_id))

# View all appointments
@app.route('/appointments')
def appointments():
    all_appts = Appointment.query.order_by(Appointment.created_at).all()
    return render_template("appointments.html", appointments=all_appts)

# ------------------ MAIN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Doctor.query.count() == 0:
            d1 = Doctor(name="Dr. Kumar", specialization="Cardiologist")
            d2 = Doctor(name="Dr. Priya", specialization="Dermatologist")
            db.session.add_all([d1, d2])
            db.session.commit()
    app.run(debug=True)
