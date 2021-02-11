from marshmallow import Schema, fields, validates, ValidationError

from .models import Employee, Customer, Job


class EmployeeSchema(Schema):
    name = fields.String()

    class Meta:
        model = Employee
        fields = ['id', 'name']

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValidationError('No name was given')


class CustomerSchema(Schema):
    name = fields.String()
    hourly_rate = fields.Float()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'hourly_rate']

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValidationError('No name was given')

    @validates('hourly_rate')
    def validate_hourly_rate(self, hourly_rate):
        if hourly_rate <= 0:
            raise ValidationError('Hourly rate must be a positive number')


class JobSchema(Schema):
    class Meta:
        model = Job
        fields = [
            'id', 'customer', 'employees', 'date', 'start_time', 'hours_number'
        ]
