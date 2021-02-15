from flask import jsonify, request
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Customer
from src.accounting.schemas import CustomerSchema
from src.accounting.utils import update_person


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
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "A customer doesn't exist.",
            'path': request.path,
        }), 404

    result = customer_schema.dump(customer)

    return jsonify(result), 200


@app.route('/customers', methods=['POST'])
def create_customer():
    customer_schema = CustomerSchema()
    try:
        customer_schema.load(request.json)

    except ValidationError as e:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': e.messages,
            'path': request.path,
        }), 400

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
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "A customer doesn't exist.",
            'path': request.path,
        }), 404

    try:
        customer_schema.load(request.json, partial=True)

    except ValidationError as e:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': e.messages,
            'path': request.path,
        }), 400

    update_person(customer, request.json)
    db.session.commit()

    result = customer_schema.dump(customer)

    return jsonify(result), 200


@app.route('/customers/<int:pk>', methods=['DELETE'])
def destroy_customer(pk):
    customer = Customer.query.get(pk)
    customer_schema = CustomerSchema()
    if not customer:
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "A customer doesn't exist.",
            'path': request.path,
        }), 404

    db.session.delete(customer)
    db.session.commit()

    result = customer_schema.dump(customer)

    return jsonify(result), 200
