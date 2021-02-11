from flask import jsonify, request
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Customer
from src.accounting.schemas import CustomerSchema
from src.accounting.utils import update_model


@app.route('/customers', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    customers_schema = CustomerSchema(many=True)

    result = customers_schema.dump(customers)

    return jsonify(result), 200


@app.route('/customers/<int:pk>', methods=['GET'])
def retrieve_customer(pk):
    customer = Customer.query.get(pk)
    customer_schema = CustomerSchema()

    if not customer:
        return jsonify({'error': {'detail': "A customer doesn't exist"}}), 404

    result = customer_schema.dump(customer)

    return jsonify(result), 200


@app.route('/customers', methods=['POST'])
def create_customer():
    customer_schema = CustomerSchema()
    if not request.json:
        return jsonify({'error': {'detail': "No data has been sent"}}), 400

    try:
        customer_schema.load(request.json)

    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    customer = Customer(**request.json)
    db.session.add(customer)
    db.session.commit()
    result = customer_schema.dump(customer)

    return jsonify(result), 201


@app.route('/customers/<int:pk>', methods=['PATCH'])
def partial_update_customer(pk):
    customer = Customer.query.get(pk)
    customer_schema = CustomerSchema()
    if not customer:
        return jsonify({'error': {'detail': "A customer doesn't exist"}}), 404

    if not request.json:
        return jsonify({'error': {'detail': "No data has been sent"}}), 400

    try:
        customer_schema.load(request.json)

    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    update_model(customer, request.json)
    db.session.commit()

    result = customer_schema.dump(customer)

    return jsonify(result), 200
