from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Job


class JobSchema(Schema):
    customer = fields.Integer(required=True)
    employees = fields.String(required=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    hours_number = fields.Float(required=True)

    class Meta:
        model = Job
        fields = [
            'id', 'customer', 'employees', 'date', 'start_time', 'hours_number'
        ]
