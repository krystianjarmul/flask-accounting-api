from marshmallow import Schema, fields, validates, ValidationError

from .models import Employee, Customer


class EmployeeSchema(Schema):
    name = fields.String(required=True)

    class Meta:
        model = Employee
        fields = ['id', 'name']

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValidationError('No name was given')


class CustomerSchema(Schema):
    name = fields.String(required=True)
    hourly_rate = fields.Float(required=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'hourly_rate']