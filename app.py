from flask import Flask, request, jsonify
from models import db, User, Salon, Service, Appointment
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ساخت آرایشگاه
@app.route('/api/salon', methods=['POST'])
def create_salon():
    data = request.get_json()
    salon = Salon(
        owner_user_id=data['owner_user_id'],
        name=data['name'],
        logo_url=data.get('logo_url', ''),
        description=data.get('description', ''),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        unique_code=data['unique_code'],
        payment_methods=str(data['payment_methods']),
        license_status='active',
        license_expiry_date=datetime.utcnow(),
        sms_credit=100,
        created_at=datetime.utcnow()
    )
    db.session.add(salon)
    db.session.commit()
    return jsonify({"message": "Salon created successfully!"})

# گرفتن اطلاعات آرایشگاه
@app.route('/api/salon/<string:code>', methods=['GET'])
def get_salon(code):
    salon = Salon.query.filter_by(unique_code=code).first()
    if salon:
        services = Service.query.filter_by(salon_id=salon.id).all()
        return jsonify({
            "salon": {
                "name": salon.name,
                "description": salon.description,
                "logo_url": salon.logo_url,
                "payment_methods": salon.payment_methods,
            },
            "services": [{"name": s.name, "price": s.price} for s in services]
        })
    return jsonify({"message": "Salon not found"}), 404

# ثبت نوبت
@app.route('/api/appointment', methods=['POST'])
def create_appointment():
    data = request.get_json()
    appointment = Appointment(
        salon_id=data['salon_id'],
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        service_id=data['service_id'],
        date=datetime.strptime(data['date'], "%Y-%m-%d").date(),
        time=datetime.strptime(data['time'], "%H:%M").time(),
        payment_method=data['payment_method'],
        payment_status='pending',
        created_at=datetime.utcnow()
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)