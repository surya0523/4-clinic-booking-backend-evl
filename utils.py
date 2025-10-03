from flask_mail import Message
from .app import mail, create_app 
# தேவையான modules-ஐ இறக்குமதி செய்க
from datetime import datetime, timedelta 


# இந்த function-ஐதான் booking confirmation மற்றும் reminder-க்கு பயன்படுத்துவீர்கள்
def send_email_notification(recipient, subject, body):
    msg = Message(subject, recipients=[recipient], body=body)
    
    app = create_app() 
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Mail failed to send: {e}") 

# Example Reminder Logic
def send_appointment_reminders():
    from .models import Slot, Booking, db
    
    # நாளைக்கான (Next Day) Slots-ஐக் கண்டறிதல்
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    
    reminder_slots = Slot.query.join(Booking).filter(
        db.func.date(Slot.start_time) == tomorrow, 
        Slot.is_booked == True
    ).all()

    for slot in reminder_slots:
        subject = "Appointment Reminder"
        body = f"Hello {slot.booking.patient.username},\n\nYour appointment with Dr. {slot.doctor.user.username} is scheduled for tomorrow at {slot.start_time.strftime('%H:%M')}."
        send_email_notification(slot.booking.patient.email, subject, body)
        print(f"Reminder sent to {slot.booking.patient.email}")