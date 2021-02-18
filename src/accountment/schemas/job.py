from marshmallow import Schema, fields

from src.accountment.models import Job
from src.accountment.schemas import CustomerSchema, EmployeeSchema


class JobSchema(Schema):
    id = fields.Integer()
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time()
    hours_number = fields.Float(required=True)

    customer = fields.Nested(CustomerSchema)
    employees = fields.Nested(EmployeeSchema, many=True)
