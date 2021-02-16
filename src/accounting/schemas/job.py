from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Job
from src.accounting.schemas import CustomerSchema, EmployeeSchema


class JobSchema(Schema):
    id = fields.Integer()
    customer_id = fields.Integer()
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    hours_number = fields.Float(required=True)

    # customer = fields.Nested(CustomerSchema)
    # employees = fields.Nested(EmployeeSchema, many=True)
