from marshmallow import Schema, fields, validates, ValidationError

from src.accounting.models import Customer


class AssignSchema(Schema):
    customer_id = fields.Integer()

    @validates('customer_id')
    def validate_customer_id(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            raise ValidationError('Not match.')
