from typing import Tuple

from flask import jsonify, request, Response, abort
from marshmallow import ValidationError

from src.accountment import app, db
from src.accountment.models import Customer
from src.accountment.schemas import CustomerSchema
from src.accountment.utils import update_person


# TODO dodac srodowisko produkcyjne (+ postgres)
# TODO dodac docker i docker-compose
# TODO rozwinac readme
# TODO dodac swagger


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
        abort(404, "A customer doesn't exist.")

    result = customer_schema.dump(customer)

    return jsonify(result), 200


@app.route('/customers', methods=['POST'])
def create_customer() -> Tuple[Response, int]:
    customer_schema = CustomerSchema()
    errors = customer_schema.validate(request.json)
    if errors:
        abort(400, errors)

    customer = Customer(**request.json)
    db.session.add(customer)
    db.session.commit()
    result = customer_schema.dump(customer)

    return jsonify(result), 201


@app.route('/customers/<int:pk>', methods=['PUT'])
def update_customer(pk: int) -> Tuple[Response, int]:
    customer = Customer.query.get(pk)
    customer_schema = CustomerSchema()
    if not customer:
        abort(404, "A customer doesn't exist.")

    errors = customer_schema.validate(request.json)
    if errors:
        abort(400, errors)

    update_person(customer, request.json)
    db.session.commit()

    result = customer_schema.dump(customer)

    return jsonify(result), 200


@app.route('/customers/<int:pk>', methods=['DELETE'])
def destroy_customer(pk: int) -> Tuple[Response, int]:
    customer = Customer.query.get(pk)
    customer_schema = CustomerSchema()
    if not customer:
        abort(404, "A customer doesn't exist.")

    db.session.delete(customer)
    db.session.commit()

    result = customer_schema.dump(customer)

    return jsonify(result), 200
