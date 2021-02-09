from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

ma = Marshmallow(app)

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


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name']


@app.route('/employees/', methods=['GET'])
def list_employee():
    employees = Employee.query.all()
    employees_schema = EmployeeSchema(many=True)

    result = employees_schema.dump(employees)

    return jsonify(result), 200
