import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key-123'
    
    # SQLite Database Configuration (Simple setup)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clinic.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Reminders Configuration (Needed for option 3)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = 'noreply@clinic.com'