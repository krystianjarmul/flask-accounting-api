from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError, validates

app = Flask(__name__)


if app.config['ENV'] == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
db.create_all()


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name: str):
        self.name = name


class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValidationError('No name was given')
        elif not isinstance(name, str):
            raise ValidationError('The given name is not of type string')


@app.route('/employees/', methods=['GET'])
def list_employee():
    employees = Employee.query.all()
    employees_schema = EmployeeSchema(many=True)

    result = employees_schema.dump(employees)

    return jsonify(result), 200


@app.route('/employees/<int:employee_id>')
def retrieve_employee(employee_id):
    employee = Employee.query.get(employee_id)
    employee_schema = EmployeeSchema()
    if employee is None:
        return jsonify({'error': 'An employee does not exist.'}), 404

    result = employee_schema.dump(employee)

    return result, 200


@app.route('/employees/', methods=['POST'])
def create_employee():
    employee = Employee(request.json['name'])
    employee_schema = EmployeeSchema()

    try:
        result = employee_schema.load(request.json)
    except ValidationError as e:
        return e.messages, 400
    db.session.add(employee)
    db.session.commit()


    return result, 201
