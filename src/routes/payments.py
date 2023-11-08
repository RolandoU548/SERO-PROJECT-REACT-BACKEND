from models import db, Payment
from flask import Blueprint, request, jsonify
from models import db, Payment
from utils import APIException


payments = Blueprint("payments", __name__)

# GET all payments
@payments.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([p.serialize() for p in payments]), 200

# POST a new payment
@payments.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not data:
        raise APIException('No input data provided', status_code=400)
    try:
        payment = Payment(
            amount=data['amount'],
            description=data['description'],
            date=data['date'],
            service=data['service'],
            invoice=data['invoice'],
            client_id=data['client'],
            status=data['status'],
            method=data['method'],
        )
        
        db.session.add(payment)
        db.session.commit()
        return jsonify(payment.serialize()), 201
    except KeyError as e:
        raise APIException(f'Missing required field: {e}', status_code=400)

# PUT an existing payment
@payments.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        raise APIException('Payment not found', status_code=404)
    data = request.get_json()
    for key, value in data.items():
        setattr(payment, key, value)
    db.session.commit()
    return jsonify(payment.serialize()), 200

# DELETE a payment
@payments.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        raise APIException('Payment not found', status_code=404)
    db.session.delete(payment)
    db.session.commit()
    return '', 204

