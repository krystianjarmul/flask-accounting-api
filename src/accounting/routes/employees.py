from flask import jsonify, request
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Employee
from src.accounting.schemas import EmployeeSchema
from src.accounting.utils import update_person


@app.route('/employees', methods=['GET'])
def list_employee():
    employees = Employee.query.all()
    employees_schema = EmployeeSchema(many=True)

    result = employees_schema.dump(employees)

    return jsonify(result), 200


@app.route('/employees/<int:pk>')
def retrieve_employee(pk):
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if not employee:
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "An employee doesn't exist.",
            'path': request.path,
        }), 404

    result = employee_schema.dump(employee)

    return jsonify(result), 200


@app.route('/employees', methods=['POST'])
def create_employee():
    employee_schema = EmployeeSchema()

    try:
        employee_schema.load(request.json)

    except ValidationError as e:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': e.messages,
            'path': request.path,
        }), 400

    employee = Employee(**request.json)
    db.session.add(employee)
    db.session.commit()

    result = employee_schema.dump(employee)

    return jsonify(result), 201


@app.route('/employees/<int:pk>', methods=['PATCH'])
def partial_update_employee(pk):
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if not employee:
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "An employee doesn't exist.",
            'path': request.path,
        }), 404

    try:
        employee_schema.load(request.json, partial=True)

    except ValidationError as e:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': e.messages,
            'path': request.path,
        }), 400

    update_person(employee, request.json)
    db.session.commit()

    result = employee_schema.dump(employee)

    return jsonify(result), 200


@app.route('/employees/<int:pk>', methods=['DELETE'])
def destroy_employee(pk):
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if not employee:
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "An employee doesn't exist.",
            'path': request.path,
        }), 404

    db.session.delete(employee)
    db.session.commit()

    result = employee_schema.dump(employee)

    return jsonify(result), 200
