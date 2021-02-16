from .. import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    jobs = db.relationship(
        'Job',
        secondary='assignments',
        cascade='all'
    )

    def __init__(self, name: str):
        self.name = name
