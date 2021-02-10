from flask import jsonify
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Customer
from src.accounting.schemas import CustomerSchema


@app.route('/customers', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    customers_schema = CustomerSchema(many=True)

    result = customers_schema.dump(customers)

    return jsonify(result), 200
