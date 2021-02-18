from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    hours_number = fields.Float()
