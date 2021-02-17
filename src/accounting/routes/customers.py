from typing import Tuple

from flask import jsonify, request, Response
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Customer
from src.accounting.schemas import CustomerSchema
from src.accounting.utils import update_person


# TODO dodac error handling decorators
# TODO dodac komende managera do testow
# TODO dodac nadpisywanie customera
# TODO dodac odpisywanie employera

@app.route('/customers', methods=['GET'])
def list_customers() -> Tuple[Response, int]:
    customers = Customer.query.all()
    customers_schema = CustomerSchema(many=True)

    result = customers_schema.dump(customers)

    return jsonify(result), 200


@app.route('/customers/<int:pk>', methods=['GET'])
def retrieve_customer(pk: int) -> Tuple[Response, int]:
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
def create_customer() -> Tuple[Response, int]:
    customer_schema = CustomerSchema()
    errors = customer_schema.validate(request.json)
    if errors:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': errors,
            'path': request.path,
        }), 400

    customer = Customer(**request.json)
    db.session.add(customer)
    db.session.commit()
    result = customer_schema.dump(customer)

    return jsonify(result), 201


@app.route('/customers/<int:pk>', methods=['PATCH'])
def partial_update_customer(pk: int) -> Tuple[Response, int]:
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

    errors = customer_schema.validate(request.json, partial=True)
    if errors:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': errors,
            'path': request.path,
        }), 400

    update_person(customer, request.json)
    db.session.commit()

    result = customer_schema.dump(customer)

    return jsonify(result), 200


@app.route('/customers/<int:pk>', methods=['DELETE'])
def destroy_customer(pk: int) -> Tuple[Response, int]:
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
