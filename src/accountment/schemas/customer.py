from marshmallow import Schema, fields, validates, ValidationError


class CustomerSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    hourly_rate = fields.Float(required=True)

    @validates('hourly_rate')
    def validate_hourly_rate(self, hourly_rate: float):
        if hourly_rate <= 0:
            raise ValidationError('Not a positive number.')
