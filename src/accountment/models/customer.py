from .. import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    hourly_rate = db.Column(db.Float)

    jobs = db.relationship('Job', backref='customer', passive_deletes=True)

    def __init__(self, name: str, hourly_rate: float):
        self.name = name
        self.hourly_rate = hourly_rate

    def __repr__(self) -> str:
        return f'Customer id: {self.id} name: {self.name}'
