from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Employee


class EmployeeSchema(Schema):
    name = fields.String(required=True)

    class Meta:
        model = Employee
        fields = ['id', 'name']
