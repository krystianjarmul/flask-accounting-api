from . import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name: str):
        self.name = name


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    hourly_rate = db.Column(db.Float)

    def __init__(self, name: str, hr: float):
        self.name = name
        self.hourly_rate = hr
