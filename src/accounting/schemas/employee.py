from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Employee


class EmployeeSchema(Schema):
    name = fields.String()

    class Meta:
        model = Employee
        fields = ['id', 'name']

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValidationError('No name was given')
