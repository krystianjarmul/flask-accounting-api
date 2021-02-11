from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Job


class JobSchema(Schema):
    class Meta:
        model = Job
        fields = [
            'id', 'customer', 'employees', 'date', 'start_time', 'hours_number'
        ]
