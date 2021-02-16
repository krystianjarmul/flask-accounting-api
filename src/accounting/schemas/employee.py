from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Employee


class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
