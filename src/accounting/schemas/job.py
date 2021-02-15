from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Job
from src.accounting.schemas import CustomerSchema


class JobSchema(Schema):
    customer_id = fields.Integer(required=True)
    employee_ids = fields.String(required=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    hours_number = fields.Float(required=True)
    customer = fields.Nested(CustomerSchema)

    class Meta:
        model = Job
        fields = [
            'id',
            'customer_id',
            'employee_ids',
            'date',
            'start_time',
            'hours_number',
            'customer'
        ]
