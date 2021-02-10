from marshmallow import Schema, fields, validates, ValidationError

from .models import Employee


class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

    class Meta:
        model = Employee
        fields = ['id', 'name']

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValidationError('No name was given')


class CustomerSchema(Schema):
    class Meta:
        fields = ['id', 'name', 'hourly_rate']