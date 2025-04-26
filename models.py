from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(100))
    role = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    logo_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    unique_code = db.Column(db.String(100), unique=True)
    payment_methods = db.Column(db.Text)  # JSON string
    card_number = db.Column(db.String(30))
    license_status = db.Column(db.String(20))
    license_expiry_date = db.Column(db.DateTime)
    sms_credit = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'))
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    duration_minutes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'))
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    payment_method = db.Column(db.String(20))
    payment_status = db.Column(db.String(20))
    payment_proof_url = db.Column(db.String(255))
    payment_verified = db.Column(db.Boolean, default=False)
    remind_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)