from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Job


class JobSchema(Schema):
    customer = fields.Integer()
    employees = fields.String()
    date = fields.Date()
    start_time = fields.Time()
    hours_number = fields.Float()

    class Meta:
        model = Job
        fields = [
            'id', 'customer', 'employees', 'date', 'start_time', 'hours_number'
        ]
