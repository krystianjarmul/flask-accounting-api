from typing import Tuple

from flask import jsonify, request, Response, abort
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Employee
from src.accounting.schemas import EmployeeSchema
from src.accounting.utils import update_person


@app.route('/employees', methods=['GET'])
def list_employee() -> Tuple[Response, int]:
    employees = Employee.query.all()
    employees_schema = EmployeeSchema(many=True)

    result = employees_schema.dump(employees)

    return jsonify(result), 200


@app.route('/employees/<int:pk>')
def retrieve_employee(pk: int) -> Tuple[Response, int]:
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if not employee:
        abort(404, "An employee doesn't exist.")

    result = employee_schema.dump(employee)

    return jsonify(result), 200


@app.route('/employees', methods=['POST'])
def create_employee() -> Tuple[Response, int]:
    employee_schema = EmployeeSchema()
    errors = employee_schema.validate(request.json)
    if errors:
        abort(400, errors)

    employee = Employee(**request.json)
    db.session.add(employee)
    db.session.commit()

    result = employee_schema.dump(employee)

    return jsonify(result), 201


@app.route('/employees/<int:pk>', methods=['PUT'])
def update_employee(pk: int) -> Tuple[Response, int]:
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if not employee:
        abort(404, "An employee doesn't exist.")

    errors = employee_schema.validate(request.json)
    if errors:
        abort(400, errors)

    update_person(employee, request.json)
    db.session.commit()

    result = employee_schema.dump(employee)

    return jsonify(result), 200


@app.route('/employees/<int:pk>', methods=['DELETE'])
def destroy_employee(pk: int) -> Tuple[Response, int]:
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if not employee:
        abort(404, "An employee doesn't exist.")

    db.session.delete(employee)
    db.session.commit()

    result = employee_schema.dump(employee)

    return jsonify(result), 200
