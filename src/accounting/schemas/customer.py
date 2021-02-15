from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Customer


class CustomerSchema(Schema):
    name = fields.String(required=True)
    hourly_rate = fields.Float(required=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'hourly_rate']

    @validates('hourly_rate')
    def validate_hourly_rate(self, hourly_rate):
        if hourly_rate <= 0:
            raise ValidationError('Hourly rate must be a positive number')
