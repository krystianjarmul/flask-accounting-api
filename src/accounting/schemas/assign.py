from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Customer, Employee


class AssignSchema(Schema):
    customer_id = fields.Integer()
    employee_id = fields.Integer()

    @validates('customer_id')
    def validate_customer_id(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            raise ValidationError('Not a matching integer.')

    @validates('employee_id')
    def validate_employee_id(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            raise ValidationError('Not a matching integer.')
