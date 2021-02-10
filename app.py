from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError, validates

# init
app = Flask(__name__)

if app.config['ENV'] == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# db
db = SQLAlchemy(app)
db.create_all()


# models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name: str):
        self.name = name


# serializers
class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

    class Meta:
        model = Employee

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValidationError('No name was given')


# routes / views
@app.route('/employees/', methods=['GET'])
def list_employee():
    employees = Employee.query.all()
    employees_schema = EmployeeSchema(many=True)

    result = employees_schema.dump(employees)

    return jsonify(result), 200


@app.route('/employees/<int:pk>')
def retrieve_employee(pk):
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if employee is None:
        return jsonify({'error': {'detail': "An employee doesn't exist"}}), 404

    result = employee_schema.dump(employee)

    return result, 200


@app.route('/employees/', methods=['POST'])
def create_employee():
    employee_schema = EmployeeSchema()
    try:
        employee_schema.load(request.json)

    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    employee = Employee(**request.json)
    db.session.add(employee)
    db.session.commit()
    result = employee_schema.dump(employee)

    return result, 201


@app.route('/employees/<int:pk>', methods=['PATCH'])
def partial_update_employee(pk):
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if employee is None:
        return jsonify({'error': {'detail': "An employee doesn't exist"}}), 404

    try:
        employee_schema.load(request.json)

    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    employee.name = request.json['name']
    db.session.commit()
    result = employee_schema.dump(employee)

    return result, 200


@app.route('/employees/<int:pk>', methods=['DELETE'])
def destroy_employee(pk):
    employee = Employee.query.get(pk)
    employee_schema = EmployeeSchema()
    if employee is None:
        return jsonify({'error': {'detail': "An employee doesn't exist"}}), 404

    db.session.delete(employee)
    db.session.commit()

    result = employee_schema.dump(employee)

    return result, 200
